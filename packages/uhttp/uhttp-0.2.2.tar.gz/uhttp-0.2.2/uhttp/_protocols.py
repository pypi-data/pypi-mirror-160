import asyncio
import base64
import hashlib
import itertools
import json
import logging
import os
import random
import struct
from collections import deque
from ssl import SSLContext, SSLError, create_default_context
from types import TracebackType
from typing import (
    AsyncGenerator,
    AsyncIterable,
    Dict,
    List,
    Type,
    Tuple,
    Union
)

import h11
import wsproto
import wsproto.extensions
import wsproto.utilities
from attrs import define, field
from attrs.validators import ge, gt, le, instance_of
from wsproto.events import (
    CloseConnection,
    Event,
    Message,
    Ping,
    Pong,
)

from ._enums import (
    HttpState,
    ProtocolState,
    WebsocketReasonPhrase,
    WebsocketState
)
from ._exceptions import (
    AtEOF,
    ConnectionAcquireTimeout,
    ConnectionClosing,
    ConnectionFailed,
    ConnectionLost,
    ConnectionLostError,
    ConnectTimeout,
    InvalidHandshake,
    LocalProtocolError,
    RemoteProtocolError,
    ReadTimeout,
    WriteTimeout
)
from ._models import (
    Auth,
    H11Response,
    H11PoolResponse,
    Origin,
    Request,
    RequestStatus,
    WebsocketMessage
)
from ._types import JSONType
from ._util import (
    ge_or_none,
    gt_or_none,
    instance_of_or_none,
    toggle_bool
)



ACCEPT_GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
ACQUIRE_CONNECTION_TIMEOUT = 10
BACKOFF_FACTOR = 1.618
BACKOFF_INITIAL = 5
BACKOFF_MAX = 60
CHUNK_SIZE = 2**16
CLOSE_HANDSHAKE_TIMEOUT = 5
CONNECT_TIMEOUT = 5
FLUSH_TIMEOUT = 5
HAPPY_EYEBALLS_DELAY = 0.25
MAX_BUFFERED_MESSAGES = 500
MAX_RECONNECT_ATTEMPTS = 5
PING_INTERVAL = 20
PING_TIMEOUT = 20
READ_BUF_LIMIT = 2 ** 16
SSL_HANDSHAKE_TIMEOUT = 3
SSL_SHUTDOWN_TIMEOUT = 0.25
WRITE_BUF_LIMIT = 2 ** 16


@define
class BaseProtocol(asyncio.Protocol):
    """
    Asynchronous stream reader/writer protocol implementation

    Parameters
    - origin (Origin): the scheme, host, port combination to establish a
    connection to
    - ssl (SSLContext): the ssl context to use for a secure connection. If
    unspecified, `ssl.create_default_context` will be used
    - connect_timeout (int, float, None): the time in seconds to wait for a
    TCP connection to be established to the remote host. If `None`, wait
    indefinitely
    - flush_timeout (int, float, None): the time in seconds to wait for the
    transport's write buffer to flush before aborting the connection
    - ssl_handshake_timeout (int, float, None): the time in seconds to wait for
    the TLS handshake to complete before aborting the connection
    - ssl_shutdown_timeout (int, float, None): the time in seconds to wait for
    the TLS closing handshake to complete before aborting the connection
    - happy_eyeballs_delay (int, float, None): the time in seconds to wait for
    a connection attempt to complete, before starting the next attempt in parallel
    - read_buf_limit (int): the low water mark limit in bytes that the protocol
    will buffer before resuming reading from the transport. The high water mark
    is 2x this limit. At which point, reading from the transport will be paused
    - write_buf_limit: the high water mark limit in bytes that the transport
    will buffer before pausing writing on the protocol
    - logger (logging.Logger): logger to use on protocol
    - loop (asyncio.AbstractEventLoop): event loop to use on protocol
    """
    origin: Origin
    ssl: SSLContext = field(default=None, validator=instance_of_or_none(SSLContext))
    connect_timeout: Union[int, float, None] = field(
        default=CONNECT_TIMEOUT,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    flush_timeout: Union[int, float] = field(
        default=FLUSH_TIMEOUT,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    ssl_handshake_timeout: Union[int, float, None] = field(
        default=SSL_HANDSHAKE_TIMEOUT,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    ssl_shutdown_timeout: Union[int, float, None] = field(
        default=SSL_SHUTDOWN_TIMEOUT,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    happy_eyeballs_delay: Union[int, float, None] = field(
        default=HAPPY_EYEBALLS_DELAY,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    read_buf_limit: int = field(
        default=READ_BUF_LIMIT, validator=[instance_of(int), ge(1024), le(2**16)]
    )
    write_buf_limit: int = field(
        default=WRITE_BUF_LIMIT, validator=[instance_of(int), ge(1024), le(2**32)]
    )
    logger: logging.Logger = field(
        factory=lambda: logging.getLogger(__name__),
        validator=instance_of(logging.Logger)
    )
    loop: asyncio.AbstractEventLoop = field(
        factory=asyncio.get_event_loop,
        validator=instance_of(asyncio.AbstractEventLoop)
    )
    _abort_handle: asyncio.TimerHandle = field(default=None, init=False)
    _buffer: bytearray = field(factory=bytearray, init=False)
    _drain_waiter: asyncio.Future = field(default=None, init=False)
    _flush_waiter: asyncio.Future = field(default=None, init=False)
    _closed_waiter: asyncio.Future = field(default=None, init=False)
    _connection_lock: asyncio.Lock = field(factory=asyncio.Lock, init=False)
    _eof: bool = field(default=False, init=False)
    _exception: Exception = field(default=None, init=False)
    _interrupt_gen: AsyncGenerator[None, None] = field(default=None, init=False)
    _keepalive_expiry: float = field(default=None, init=False)
    _over_ssl: bool = field(default=False, init=False)
    _read_paused: bool = field(default=False, init=False)
    _read_waiter: asyncio.Future = field(default=None, init=False)
    _protocol_state: ProtocolState = field(default=ProtocolState.CLOSED, init=False)
    _transport: asyncio.Transport = field(default=None, init=False)

    def __attrs_post_init__(self) -> None:
        self.set_ssl_settings()

    @property
    def transport(self) -> asyncio.Transport:
        return self._transport

    @property
    def peercert(self) -> Union[Dict[str, str], None]:
        if self._transport is not None:
            return self._transport.get_extra_info('peercert')
        
    @property
    def peercert_b(self) -> Union[bytes, None]:
        peercert = self.peercert
        if peercert is not None:
            return json.dumps(peercert).encode()

    async def aconnect(self) -> None:
        """
        Asynchronously establish connection to remote host. Cancelling this
        coroutine is discouraged. Reduce the `connect_timeout` parameter instead

        Parameters
        - None

        Returns
        - None

        Raises
        - ConnectTimeout: failed to establish connection in `connect_timeout`
        seconds
        - ConnectionFailed: failed to establish a connection due to an exception.
        This is usually due to an OSError
        - RuntimeError: protocol is not in CLOSED state
        """
        async with self._connection_lock:
            if self._protocol_state is not ProtocolState.CLOSED:
                raise RuntimeError(
                    f"Invalid state to establish connection {self._protocol_state.name}"
                )
            self._protocol_state = ProtocolState.CONNECTING
            await self.cancel_interrupt_helper()
            try:
                await asyncio.wait_for(
                    self.loop.create_connection(
                        lambda: self,
                        host=self.origin.host,
                        port=self.origin.port,
                        ssl=self.ssl,
                        ssl_handshake_timeout=self.ssl_handshake_timeout,
                        happy_eyeballs_delay=self.happy_eyeballs_delay
                    ),
                    self.connect_timeout
                )
            except asyncio.TimeoutError as err:
                # theres a (very small) possibility that connection_made can
                # be called before the timeout expires
                if self._protocol_state is ProtocolState.CONNECTED:
                    self.abort()
                self._protocol_state = ProtocolState.CLOSED
                raise ConnectTimeout(self.connect_timeout) from err
            except asyncio.CancelledError:
                # theres a (very small) possibility that connection_made can
                # be called before the cancel error is thrown but before
                # create_connection returns
                if self._protocol_state is ProtocolState.CONNECTED:
                    self.abort()
                self._protocol_state = ProtocolState.CLOSED
                raise
            except Exception as err:
                self._protocol_state = ProtocolState.CLOSED
                raise ConnectionFailed(err)
            else:
                self._interrupt_gen = self.interrupt_helper()
                await self._interrupt_gen.__anext__()

    async def aclose(self) -> None:
        """
        Asynchronously close the connection to the remote host
        
        This coroutine waits for the `connection_lost` method to be called before
        returning. Cancelling `aclose` is discouraged, instead you should reduce
        the `flush_timeout` and `ssl_shutdown_timeout` parameters
        
        The maximum amount of time this coroutine will wait before aborting the
        connection is `flush_timeout` + `ssl_shutdown_timeout seconds` (if over
        SSL) else the max time is `flush_timeout` + 0.1 seconds
        
        `aclose` is idempotent, multiple calls to `aclose` will do nothing.
        Multiple coroutines can safely await `aclose` concurrently
        
        Parameters
        - None

        Returns
        - None

        Raises
        - None
        """
        async with self._connection_lock:
            if self._protocol_state is ProtocolState.CLOSED:
                return
            elif self._protocol_state is not ProtocolState.CLOSING:
                self.close()
            waiter = self.get_close_waiter()
            await asyncio.shield(waiter)

    async def aread(self, n: int, timeout: Union[int, float, None]) -> bytes:
        """
        Asynchronously read data from transport. This coroutine can be safely
        cancelled

        Parameters
        - n (int): the max number of bytes to read from the protocol's buffer
        - timeout (Union[int, float, None]): the time to wait in seconds for
        new data to arrive if the buffer is empty

        Returns
        - bytes

        Raises
        - AtEOF: the peer has closed the read side of the connection. The write
        side is still available. This error does not close the connection. It
        is up to the higher abstracted to determine what to do with this error
        - ConnectionLost: the connection is closed
        - ConnectionLostError: the connection was closed due to an error on the
        transport
        - ReadTimeout: the timeout limit was exceeded. This does not close the
        connection
        - RuntimeError: two coroutines attempted to read data from the protocol
        concurrently. This does not close the connection
        """
        if len(self._buffer) > 0:
            return self.read(n)
        try:
            waiter = self.get_read_waiter()
        except ConnectionClosing:
            await self.aclose()
            raise self._exception
        try:
            await asyncio.wait_for(waiter, timeout)
        except asyncio.TimeoutError as err:
            raise ReadTimeout(timeout) from err
        else:
            return self.read(n)

    async def awrite(self, data: bytes, timeout: Union[int, float, None]) -> None:
        """
        Asynchronously write data to transport. Cancelling this coroutine is
        discouraged

        Parameters
        - n (int): the max number of bytes to read from the protocol's buffer
        - timeout (Union[int, float, None]): the time to wait in seconds for
        new data to arrive if the buffer is empty

        Returns
        - None

        Raises
        - ConnectionLost: the connection is closed
        - ConnectionLostError: the connection was closed due to an error on the
        transport
        - WriteTimeout: the timeout limit was exceeded. This does not close the
        connection. The transport buffer is still draining despite this error.
        A subsequent call to `awrite` may raise a `RuntimeError`
        - RuntimeError: a corutine attempted to write data while the write side
        of the protocol was paused
        """
        try:
            waiter = self.write(data)
        except ConnectionClosing:
            await self.aclose()
            raise self._exception
        else:
            if waiter is not None:
                try:
                    await asyncio.wait_for(asyncio.shield(waiter), timeout)
                except asyncio.TimeoutError as err:
                    raise WriteTimeout(timeout) from err

    async def interrupt_helper(self) -> AsyncGenerator[None, None]:
        while True:
            try:
                break_ = yield
                if break_:
                    break
            except GeneratorExit:
                # this should only happen in a KeyboardInterrupt or SystemExit
                # like exception. it ensures the socket gets closed which garbage
                # collection would do anyway but it also ensures the interrupt
                # gets raised rather than a RuntimeError from the transport
                # trying to do something on a closed loop
                if self._protocol_state is not ProtocolState.CLOSED:
                    self.logger.debug("%r: Aborting protocol on interrupt", self.origin)
                    self.abort()
                raise
    
    async def cancel_interrupt_helper(self):
        interrupt_gen = self._interrupt_gen
        self._interrupt_gen = None
        if interrupt_gen is not None:
            try:
                await interrupt_gen.asend(True)
            except StopAsyncIteration:
                await interrupt_gen.aclose()
            finally:
                del interrupt_gen

    async def wait_flushed(self) -> None:
        # useful when you want to write one last bit of data, wait for
        # that data to be sent and then abort the transport without waiting
        # for a reply. This will complete before connection_lost is called
        waiter = self._flush_waiter
        if waiter is not None and not waiter.done():
            await waiter

    def abort(self):
        if self._protocol_state is ProtocolState.CLOSED:
            return
        assert self._transport is not None
        self._transport.abort()

    def close(self) -> None:
        if self._protocol_state in (ProtocolState.CLOSED, ProtocolState.CLOSING):
            return
        self._protocol_state = ProtocolState.CLOSING
        assert self._transport is not None, "close: Transport None in CLOSING state"
        if not self._transport.is_closing():
            self._transport.close()
        # monitor the transport to ensure buffer is flushed
        self.loop.call_soon(self.flush_transport)
        self._flush_waiter = self.loop.create_future()
        # abort the transport if flush takes too long
        self.schedule_abort(self.flush_timeout)

    def read(self, n: int) -> bytes:
        # this will always return something when called including empty bytes
        data = bytes(self._buffer[:n])
        del self._buffer[:n]
        self.maybe_resume_reading()
        return data

    def write(self, data: bytes) -> Union[asyncio.Future, None]:
        self.check_can_write()
        self._transport.write(data)
        # the transport's state is updated immediately. if a fatal error
        # occurred it will immediately show as closing
        self.check_closing()
        # similarly, if the transport buffer is full, pause_writing is called
        # immediately
        if self._drain_waiter is not None:
            waiter = self._drain_waiter
            assert not waiter.done(), "write: Drain waiter done"
            return waiter

    def connection_made(self, transport: asyncio.Transport) -> None:
        assert self._abort_handle is None, "connection_made: abort handle not None"
        assert self._drain_waiter is None, "connection_made: drain waiter not None"
        assert self._read_waiter is None, "connection_made: read waiter not None"
        assert self._flush_waiter is None, "connection_made: flush waiter not None"
        self._protocol_state = ProtocolState.CONNECTED
        self._buffer.clear()
        self._eof = False
        self._exception = None
        self._over_ssl = transport.get_extra_info('sslcontext') is not None
        self._read_paused = False
        transport.set_write_buffer_limits(self.write_buf_limit)
        self._transport = transport

    def connection_lost(self, exc: Union[Exception, None]) -> None:
        # https://github.com/aio-libs/aiohttp/issues/3535#issuecomment-544279431
        if isinstance(exc, SSLError):
            if "APPLICATION_DATA_AFTER_CLOSE_NOTIFY" in exc.reason:
                exc = None
        exc = ConnectionLostError(exc) if exc is not None else ConnectionLost()
        self._protocol_state = ProtocolState.CLOSED
        self._exception = exc
        # if read() called after connection_lost while in a paused state
        # we would get an AssertionError so set read_pause to False
        self._read_paused = False
        self._transport = None
        self.cancel_handle('_abort_handle')
        self.set_future('_read_waiter', exc)
        self.set_future('_drain_waiter', exc)
        self.set_future('_flush_waiter')
        self.set_future('_closed_waiter')

    def data_received(self, data: bytes) -> None:
        assert not self._eof, "data_received: Feed data after EOF"
        self._buffer.extend(data)
        self.maybe_pause_reading()
        self.wakeup_reader()

    def eof_received(self) -> bool:
        self._eof = True
        self.wakeup_reader()
        self.logger.debug("%r: EOF received", self.origin)
        if self._over_ssl:
            # dont allow half closed connections over ssl
            return False
        return True

    def pause_writing(self) -> None:
        assert self._drain_waiter is None, "pause_writing: drain waiter None"
        self._drain_waiter = self.loop.create_future()
        self.logger.debug("%r: Paused writing", self.origin)

    def resume_writing(self) -> None:
        assert self._drain_waiter is not None and not self._drain_waiter.done(), "resume_writing: drain_waiter None or done"
        self.set_future('_drain_waiter')
        self.logger.debug("%r: Resumed writing", self.origin)

    def get_read_waiter(self) -> asyncio.Future:
        self.check_can_read()
        waiter = self.loop.create_future()
        self._read_waiter = waiter
        return waiter

    def get_close_waiter(self):
        if self._protocol_state not in (ProtocolState.CLOSED, ProtocolState.CLOSING):
            # raise error because future would never finish
            raise RuntimeError('HTTP protocol is not closed or closing')
        if self._protocol_state is ProtocolState.CLOSED:
            return
        if self._closed_waiter is None or self._closed_waiter.done():
            waiter = self.loop.create_future()
            self._closed_waiter = waiter
            return waiter
        else:
            waiter = self._closed_waiter
            return waiter

    def check_can_read(self) -> None:
        self.check_closed()
        self.check_closing()
        if self._eof:
            raise AtEOF()
        if self._read_waiter is not None:
            if not self._read_waiter.done():
                raise RuntimeError(
                    "Cannot read while another coroutine is waiting for data"
                )
            else:
                # user may have cancelled aread or timed out waiting, leaving
                # the read_waiter in a cancelled state. it should always be
                # cancelled if we get here
                assert self._read_waiter.cancelled()
                self._read_waiter = None

    def check_can_write(self) -> None:
        self.check_closed()
        self.check_closing()
        if self._drain_waiter is not None:
            raise RuntimeError("Cannot write while transport buffer is draining")

    def check_closed(self) -> None:
        if self._protocol_state is ProtocolState.CLOSED:
            if self._exception is None:
                # user tried to read/write without ever calling aconnect first
                raise RuntimeError("Connection was never established")
            raise self._exception
        if self._protocol_state is ProtocolState.CLOSING:
            raise ConnectionClosing()

    def check_closing(self) -> None:
        # this should only ever be called after check_closed
        assert self._transport is not None
        if self._transport.is_closing():
            self.close()
            raise ConnectionClosing()

    def maybe_pause_reading(self) -> None:
        if self._read_paused:
            return
        if len(self._buffer) > 2 * self.read_buf_limit:
            self._read_paused = True
            assert self._transport is not None, "maybe_pause_reading: Transport None"
            self._transport.pause_reading()
            self.logger.debug("%r: Paused reading", self.origin)

    def maybe_resume_reading(self) -> None:
        if not self._read_paused:
            return
        if len(self._buffer) < self.read_buf_limit:
            self._read_paused = False
            assert self._transport is not None, "maybe_resume_reading: Transport None"
            self._transport.resume_reading()
            self.logger.debug("%r: Resumed reading", self.origin)

    def wakeup_reader(self) -> None:
        self.set_future('_read_waiter')

    def flush_transport(self) -> None:
        if self._protocol_state is ProtocolState.CLOSED:
            return self.transport_flushed()
        try:
            buflen = self._transport.get_write_buffer_size()
        except AttributeError:
            # ssl transport closed, connection_lost will be called on
            # next loop iteration
            return self.transport_flushed()
        if buflen > 0:
            # keep scheduling method until the buffer is flushed
            self.loop.call_soon(self.flush_transport)
            self.logger.debug("Flushing %i bytes", buflen)
        else:
            self.cancel_handle('_abort_handle')
            timeout = self.ssl_shutdown_timeout or 0.1
            # if we schedule abort here it sometimes gets called immediately
            # instead of after the timeout, scheduling the scheduling of the
            # abort seems to fix this
            self.loop.call_soon(self.schedule_abort, timeout)
            self.transport_flushed()

    def transport_flushed(self) -> None:
        self.set_future('_flush_waiter')

    def schedule_abort(self, timeout: Union[int, float]) -> None:
        if self._protocol_state is not ProtocolState.CLOSED:
            self._abort_handle = self.loop.call_later(timeout, self.abort)

    def cancel_handle(self, handle: str) -> None:
        pending_handle: asyncio.Handle = getattr(self, handle, None)
        if pending_handle is not None:
            setattr(self, handle, None)
            pending_handle.cancel()

    def cancel_task(self, task: str) -> None:
        pending_task: asyncio.Task = getattr(self, task, None)
        if pending_task is not None:
            setattr(self, task, None)
            pending_task.cancel()
    
    def set_future(
        self,
        fut: str,
        exc: Union[ConnectionLost, ConnectionLostError] = None
    ) -> None:
        pending_future: asyncio.Future = getattr(self, fut, None)
        if pending_future is not None:
            setattr(self, fut, None)
            if not pending_future.done():
                if exc is None:
                    pending_future.set_result(None)
                else:
                    pending_future.set_exception(exc)

    def set_ssl_settings(self) -> None:
        if self.origin.is_secure and self.ssl is None:
            self.ssl = create_default_context()
        elif not self.origin.is_secure and self.ssl is not None:
            raise ValueError("SSL context with insecure scheme")
        elif not self.origin.is_secure and self.ssl is None:
            self.ssl_handshake_timeout = None
            self.ssl_shutdown_timeout = None


@define(slots=False)
class ReconnectMixin(BaseProtocol):
    auto_reconnect: bool = field(default=True, validator=instance_of(bool))
    max_reconnect_attempts: int = field(
        default=MAX_RECONNECT_ATTEMPTS, validator=[instance_of(int), gt(0)]
    )
    backoff_factor: Union[int, float] = field(
        default=BACKOFF_FACTOR, validator=[instance_of((int, float)), gt(0)]
    )
    initial_backoff: Union[int, float] = field(
        default=BACKOFF_INITIAL, validator=[instance_of((int, float)), gt(0)]
    )
    max_backoff: Union[int, float] = field(
        default=BACKOFF_MAX, validator=[instance_of((int, float)), gt(0)]
    )
    _client_close: bool = field(default=False, init=False)
    _reconnect_stop_waiter: asyncio.Future = field(default=None, init=False)
    _was_connected: bool = field(default=False, init=False)

    async def aclose(self) -> None:
        self._client_close = True
        return await super().aclose()

    async def reconnect(self) -> None:
        raise NotImplementedError()

    def connection_made(self, transport: asyncio.Transport) -> None:
        super().connection_made(transport)
        self._was_connected = True
        self._client_close = False

    def connection_lost(self, exc: Union[Exception, None]) -> None:
        self.set_future('_reconnect_stop_waiter')
        super().connection_lost(exc)

    def should_reconnect(self) -> bool:
        raise NotImplementedError()


@define(slots=False)
class H11Mixin(ReconnectMixin):
    chunk_size: int = field(
        default=CHUNK_SIZE, validator=[instance_of(int), gt(0)]
    )
    _http_state: HttpState = field(default=HttpState.CLOSED, init=False)
    _release: bool = field(default=True, init=False)
    _h11_state_machine: h11.Connection = field(default=None, init=False)

    @property
    def state(self) -> HttpState:
        return self._http_state

    async def arequest(self, request: Request, auth: Auth = None) -> H11Response:
        """
        Asynchronously send an HTTP/1.1 request

        Parameters
        request (Request): the request to send
        auth (Auth): the auth flow to be executed for this request. Defaults to
        no auth

        Returns
        - H11Response: an HTTP/1.1 response object. The response object can
        be iterated over to get the response content or read all at once

        Raises
        - AtEOF: EOF received from peer, could not complete response
        - ConnectionLost: the connection is closed
        - ConnectionLostError: the connection was closed due to an error on the
        transport
        - LocalProtocolError: client violated HTTP/1.1 protocol
        - RemoteProtocolError: peer violated HTTP/1.1 protocol
        - ReadTimeout: timeout reached waiting for data, could not complete
        response
        - WriteTimeout: timeout reached waiting for transport buffer to flush,
        could not complete request
        - RuntimeError: client state is not IDLE or client tried to send request
        to mismatched origin
        """
        # if the connection is lost due to a dropped connection (not because
        # aclose was called) it will remain closed until we try and make a
        # request. at which point it will try and reconnect
        if self.should_reconnect():
            connected = await self.reconnect()
            if not connected:
                assert self._exception is not None, "arequest: conn lost exc is None after reconnect attempt"
                raise self._exception
        if self._http_state is not HttpState.IDLE:
            raise RuntimeError(
                f"Invalid state to initiate request {self.state.name}"
            )
        if request.url.origin != self.origin:
            raise RuntimeError(
                f"Attempted to send request to {repr(request.url.origin)} on "
                f"connection {repr(self.origin)}"
            )
        self._http_state = HttpState.ACTIVE
        auth = auth or Auth()
        auth.set_connection(self)
        # the auth flow may send multiple requests consuming the response body
        # each time (i.e response_closed is called). We dont want the
        # the state to change to idle until the entire auth flow is complete
        with toggle_bool(self, '_release'):
            response = await self.send_handling_auth(request, auth)
        return response

    async def send_handling_auth(self, request: Request, auth: Auth) -> H11Response:
        auth_flow = auth.async_auth_flow(request)
        try:
            request = await auth_flow.__anext__()
            while True:
                response = await self.send_request(request)
                try:
                    try:
                        next_request = await auth_flow.asend(response)
                    except StopAsyncIteration:
                        return response
                except BaseException:
                    await self.aclose()
                    raise
                else:
                    await response.aread()
                    request = next_request
        finally:
            await auth_flow.aclose()

    async def send_request(self, request: Request) -> H11Response:
        try:
            self.start_next_cycle()
        except LocalProtocolError:
            await self.aclose()
            raise
        timeout = request.timeouts.get('read')
        try:
            await self.send_request_headers(request)
            await self.send_request_content(request)
            event = await self.receive_response(timeout)
        except (
            AtEOF,
            ConnectionLost,
            ConnectionLostError,
            LocalProtocolError,
            ReadTimeout,
            RemoteProtocolError,
            WriteTimeout
        ):
            await self.aclose()
            raise
        else:
            return H11Response(
                request,
                event,
                self
            )
    
    async def send_request_headers(self, request: Request) -> None:
        timeout = request.timeouts.get('write')
        event = request.to_event()
        await self.send_event(event, timeout)

    async def send_request_content(self, request: Request) -> None:
        timeout = request.timeouts.get('write')
        content = request.content
        if content is not None:
            async for chunk in content:
                event = h11.Data(chunk)
                await self.send_event(event, timeout)
        await self.send_event(h11.EndOfMessage(), timeout)

    async def receive_response(
        self,
        timeout: Union[int, float, None]
    ) -> Union[h11.Response, h11.InformationalResponse]:
        event = await self.next_event(timeout)
        if not isinstance(event, (h11.Response, h11.InformationalResponse)):
            raise RemoteProtocolError(
                f"Unexpected event ({event.__class__.__name__}) while receiving response"
            )
        return event

    async def receive_response_content(
        self,
        timeout: Union[int, float, None]
    ) -> AsyncGenerator[bytes, None]:
        while True:
            event = await self.next_event(timeout)
            if isinstance(event, h11.Data):
                yield event.data
            elif event is h11.PAUSED or isinstance(event, h11.EndOfMessage):
                break
            else:
                raise RemoteProtocolError(
                    f"Unexpected event ({event.__class__.__name__}) while receiving content"
                )

    async def send_event(
        self,
        event: h11.Event,
        timeout: Union[int, float, None]
    ) -> None:
        try:
            data = self._h11_state_machine.send(event)
        except h11.LocalProtocolError as err:
            raise LocalProtocolError(str(err))
        await self.awrite(data, timeout)

    async def next_event(self, timeout: Union[int, float, None]) -> h11.Event:
        while True:
            try:
                event = self._h11_state_machine.next_event()
            except h11.RemoteProtocolError as err:
                raise RemoteProtocolError(str(err))
            if event is h11.NEED_DATA:
                data = await self.aread(self.chunk_size, timeout)
                self._h11_state_machine.receive_data(data)
            else:
                return event

    async def response_closed(self) -> None:
        if self._release and self._http_state is HttpState.ACTIVE:
            self._http_state = HttpState.IDLE

    async def reconnect(self) -> None:
        attempts = 0
        while attempts < self.max_reconnect_attempts:
            async with self._connection_lock:
                # user may call aclose while sleeping for next reconnect attempt
                if self._client_close:
                    break
            self.logger.info(
                "Attempting reconnect. Attempt %i of %i",
                attempts + 1,
                self.max_reconnect_attempts
            )
            try:
                await self.aconnect()
            except (ConnectTimeout, ConnectionFailed) as err:
                backoff_delay = (
                    self.initial_backoff * self.backoff_factor ** attempts
                )
                backoff_delay = min(
                    self.max_backoff,
                    int(backoff_delay)
                )
                self.logger.debug(
                    "Reconnect failed. Trying again in %0.2f seconds. %r",
                    backoff_delay,
                    err
                )
                waiter = self.loop.create_future()
                self._reconnect_stop_waiter = waiter
                try:
                    await asyncio.wait_for(waiter, timeout=backoff_delay)
                except asyncio.TimeoutError:
                    self._reconnect_stop_waiter = None
                else:
                    break
                attempts += 1
            else:
                break
        if self._protocol_state is not ProtocolState.CONNECTED:
            return False
        return True

    def connection_made(self, transport: asyncio.Transport) -> None:
        super().connection_made(transport)
        self._http_state = HttpState.IDLE
        self._h11_state_machine = h11.Connection(our_role=h11.CLIENT)

    def connection_lost(self, exc: Union[Exception, None]) -> None:
        super().connection_lost(exc)
        self._http_state = HttpState.CLOSED

    def should_reconnect(self) -> bool:
        return (
            self.auto_reconnect and
            self._http_state is HttpState.CLOSED and
            not self._client_close and
            self._was_connected
        )

    def start_next_cycle(self) -> None:
        if (
            self._h11_state_machine.our_state is h11.DONE and
            self._h11_state_machine.their_state is h11.DONE
        ):
            self._h11_state_machine.start_next_cycle()
        elif (
            self._h11_state_machine.our_state is not h11.IDLE and
            self._h11_state_machine.their_state is not h11.IDLE
        ):
            raise LocalProtocolError(
                f"Cannot initiate request in state {self._h11_state_machine.states}"
            )

    def is_available(self) -> bool:
        if self._http_state is HttpState.IDLE:
            return True
        # if we can reconnect we will try on the next request. this method
        # is intended to indicate that a request can be attempted
        return self.should_reconnect()


@define(slots=False)
class H11Protocol(H11Mixin):
    """
    Asynchronous HTTP/1.1 protocol implementation

    Parameters
    - origin (Origin): the scheme, host, port combination to establish a
    connection to
    - ssl (SSLContext): the ssl context to use for a secure connection. If
    unspecified, `ssl.create_default_context` will be used
    - keepalive_timeout (int, float, None): the time in seconds to leave a
    connection open before closing it. If `None`, the connection will never expire
    (on the client side). If some number greater than 0, the keepalive expiry
    will be checked at the end of request/response cycle and the connection will
    closed if the keepalive expiry has been reached. The expiry resets on each
    request/response cycle
    - chunk_size (int): the max number of bytes to read from the transport on
    each read call
    - auto_reconnect(bool): if `True` and the peer has closed the connection, or
    a network interruption has occurred, the protocol will attempt to
    automatically re-establish a connection to the remote host
    - max_reconnect_attempts (int): if the conditions are met to attempt a
    reconnection, the protocol will attempt at most `max_reconnect_attempts` times
    before failing the protocol
    - backoff_factor (int, float): the exponential backoff delay factor to
    increment the time between reconnect attempts
    - initial_backoff (int, float): the initial time in seconds to wait after
    the first failed reconnect attempt
    - max_backoff (int, float): the max amount of time in seconds to wait for
    the next reconnect attempt
    - connect_timeout (int, float, None): the time to wait for a TCP connection
    to be established to the remote host. If `None` wait indefinitely
    - flush_timeout (int, float, None): the time in seconds to wait for the
    transport's write buffer to flush before aborting the connection
    - ssl_handshake_timeout (int, float, None): the time in seconds to wait for
    the TLS handshake to complete before aborting the connection
    - ssl_shutdown_timeout (int, float, None): the time in seconds to wait for
    the TLS closing handshake to complete before aborting the connection
    - happy_eyeballs_delay (int, float, None): the time in seconds to wait for
    a connection attempt to complete, before starting the next attempt in parallel
    - read_buf_limit (int): the low water mark limit in bytes that the protocol
    will buffer before resuming reading from the transport. The high water mark
    is 2x this limit. At which, reading from the transport will be paused
    - write_buf_limit: the high water mark limit in bytes that the transport
    will buffer before pausing writing on the protocol
    - logger (logging.Logger): logger to use on protocol
    - loop (asyncio.AbstractEventLoop): event loop to use on protocol
    """
    keepalive_timeout: Union[int, float, None] = field(
        default=None,
        validator=[instance_of_or_none((int, float)), ge_or_none(0)]
    )
    _keepalive_expiry: float = field(default=None, init=False)

    async def response_closed(self) -> None:
        if self._keepalive_expiry is not None:
            if self._keepalive_expiry < self.loop.time():
                self.logger.debug("%r: Keepalive expired", self.origin)
                return await self.aclose()
            else:
                self._keepalive_expiry = self.loop.time() + self.keepalive_timeout
        return await super().response_closed()

    def connection_made(self, transport: asyncio.Transport) -> None:
        super().connection_made(transport)
        if self.keepalive_timeout is not None:
            self._keepalive_expiry = self.loop.time() + self.keepalive_timeout


@define
class H11Pool:
    """
    Asynchronous HTTP/1.1 connection pool

    Parameters
    - origin (Origin): the scheme, host, port combination to establish a
    connection to
    - auth (Auth): the auth flow to use for requests
    - max_connections (int): the maximum number of connections to have open
    simultaneously
    - ssl (SSLContext): the ssl context to use for a secure connection. If
    unspecified, `ssl.create_default_context` will be used
    - keepalive_timeout (int, float, None): the time in seconds to leave a
    connection open before closing it. If `None`, the connection will never expire
    (on the client side). If some number greater than 0, the keepalive expiry
    will be checked at the end of request/response cycle and the connection will
    closed if the keepalive expiry has been reached. The expiry resets on each
    request/response cycle
    - acquire_connection_timeout (int, float, None): the max amount of time in
    seconds to wait for a connection to become available if the connection cap
    has been reached
    - chunk_size (int): the max number of bytes to read from the transport on
    each read call
    - auto_reconnect(bool): if `True` and the peer has closed the connection, or
    a network interruption has occurred, the protocol will attempt to
    automatically re-establish a connection to the remote host
    - max_reconnect_attempts (int): if the conditions are met to attempt a
    reconnection, the protocol will attempt at most `max_reconnect_attempts` times
    before failing the protocol
    - backoff_factor (int, float): the exponential backoff delay factor to
    increment the time between reconnect attempts
    - initial_backoff (int, float): the initial time in seconds to wait after
    the first failed reconnect attempt
    - max_backoff (int, float): the max amount of time in seconds to wait for
    the next reconnect attempt
    - connect_timeout (int, float, None): the time to wait for a TCP connection
    to be established to the remote host. If `None` wait indefinitely
    - flush_timeout (int, float, None): the time in seconds to wait for the
    transport's write buffer to flush before aborting the connection
    - ssl_handshake_timeout (int, float, None): the time in seconds to wait for
    the TLS handshake to complete before aborting the connection
    - ssl_shutdown_timeout (int, float, None): the time in seconds to wait for
    the TLS closing handshake to complete before aborting the connection
    - happy_eyeballs_delay (int, float, None): the time in seconds to wait for
    a connection attempt to complete, before starting the next attempt in parallel
    - read_buf_limit (int): the low water mark limit in bytes that the protocol
    will buffer before resuming reading from the transport. The high water mark
    is 2x this limit. At which, reading from the transport will be paused
    - write_buf_limit: the high water mark limit in bytes that the transport
    will buffer before pausing writing on the protocol
    - logger (logging.Logger): logger to use on protocol
    - loop (asyncio.AbstractEventLoop): event loop to use on protocol
    """
    origin: Origin = field(default=None, validator=instance_of_or_none(Origin))
    auth: Auth = field(default=None, validator=instance_of_or_none(Auth))
    max_connections: int = field(default=50, validator=[instance_of(int), gt(0)])
    ssl: SSLContext = field(default=None, validator=instance_of_or_none(SSLContext))
    keepalive_timeout: Union[int, float, None] = field(
        default=None,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    acquire_connection_timeout: Union[int, float, None] = field(
        default=ACQUIRE_CONNECTION_TIMEOUT,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    connect_timeout: Union[int, float, None] = field(
        default=CONNECT_TIMEOUT,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    flush_timeout: Union[int, float] = field(
        default=FLUSH_TIMEOUT,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    ssl_handshake_timeout: Union[int, float, None] = field(
        default=SSL_HANDSHAKE_TIMEOUT,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    ssl_shutdown_timeout: Union[int, float, None] = field(
        default=SSL_SHUTDOWN_TIMEOUT,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    happy_eyeballs_delay: Union[int, float, None] = field(
        default=HAPPY_EYEBALLS_DELAY,
        validator=[instance_of_or_none((int, float)), gt_or_none(0)]
    )
    read_buf_limit: int = field(
        default=READ_BUF_LIMIT, validator=[instance_of(int), ge(1024), le(2**16)]
    )
    write_buf_limit: int = field(
        default=WRITE_BUF_LIMIT, validator=[instance_of(int), ge(1024), le(2**32)]
    )
    auto_reconnect: bool = field(default=True, validator=instance_of(bool))
    max_reconnect_attempts: int = field(
        default=MAX_RECONNECT_ATTEMPTS, validator=[instance_of(int), gt(0)]
    )
    backoff_factor: Union[int, float] = field(
        default=BACKOFF_FACTOR, validator=[instance_of((int, float)), gt(0)]
    )
    initial_backoff: Union[int, float] = field(
        default=BACKOFF_INITIAL, validator=[instance_of((int, float)), gt(0)]
    )
    max_backoff: Union[int, float] = field(
        default=BACKOFF_MAX, validator=[instance_of((int, float)), gt(0)]
    )
    chunk_size: int = field(default=CHUNK_SIZE, validator=[instance_of(int), ge(0)])
    logger: logging.Logger = field(
        factory=lambda: logging.getLogger(__name__),
        validator=instance_of(logging.Logger)
    )
    loop: asyncio.AbstractEventLoop = field(
        factory=asyncio.get_event_loop,
        validator=instance_of(asyncio.AbstractEventLoop)
    )
    _available: List[H11Protocol] = field(factory=list, init=False)
    _busy: List[H11Protocol] = field(factory=list, init=False)
    _pool_lock: asyncio.Lock = field(factory=asyncio.Lock, init=False)
    _requests: List[RequestStatus] = field(factory=list, init=False)

    @property
    def num_connections(self) -> int:
        return len(self._available) + len(self._busy)

    async def arequest(self, request: Request, auth: Auth = None) -> H11PoolResponse:
        """
        Asynchronously submit a request to the connection pool

        Parameters
        request (Request): the request to send
        auth (Auth): the auth float to be executed for this request. Defaults to
        no auth

        Returns
        - HttpPoolResponse: an HTTP response object. The response object can
        be iterated over to get the response content

        Raises
        - AtEOF: EOF received from peer, could not complete response
        - ConnectionLost: the connection is closed
        - ConnectionLostError: the connection was closed due to an error on the
        transport
        - ConnectionAcquireTimeout: timeout expired waiting to acquire a connection
        from the pool
        - LocalProtocolError: client violated HTTP/1.1 protocol
        - RemoteProtocolError: peer violated HTTP/1.1 protocol
        - ReadTimeout: timeout reached waiting for data, could not complete
        response
        - WriteTimeout: timeout reached waiting for transport buffer to flush,
        could not complete request
        - RuntimeError: tried to send a request without an origin
        """
        self.prep_request_origin(request)
        if not request.url.is_http:
            raise RuntimeError(f"Invalid scheme {request.url.scheme}://")
        auth = auth or self.auth or Auth()
        status = RequestStatus(request)
        async with self._pool_lock:
            self._requests.append(status)
            self.remove_closed_connections()
            await self.attempt_to_acquire_connection(status)
        while True:
            try:
                connection = await asyncio.wait_for(
                    status.wait_for_connection(),
                    self.acquire_connection_timeout
                )
            except asyncio.TimeoutError:
                self._requests.remove(status)
                raise ConnectionAcquireTimeout(self.acquire_connection_timeout)
            try:
                response = await connection.arequest(request, auth)
            except BaseException:
                await self.response_closed(status)
                raise
            else:
                break
        return H11PoolResponse(
            status,
            self,
            response
        )

    async def aclose(self) -> None:
        """
        Asynchronously close the connection pool. This coroutine closes all
        connections in the pool concurrently
        
        Parameters
        - None

        Returns
        - None

        Raises
        - RuntimeError: the connection pool was closed with requests still in
        flight
        """
        async with self._pool_lock:
            requests_still_in_flight = len(self._requests)
            closers = [
                connection.aclose() for connection in
                itertools.chain(self._available, self._busy)
            ]
            await asyncio.gather(*closers)
            self._available = list()
            self._busy = list()
            self._requests = list()
            if requests_still_in_flight:
                raise RuntimeError(
                    f"The connection pool was closed while {requests_still_in_flight} "
                    f"HTTP requests/responses were still in-flight."
                )

    async def attempt_to_acquire_connection(self, status: RequestStatus) -> bool:
        origin = status.request.url.origin
        waiting = [s for s in self._requests if s.connection is None]
        # handle requests strictly in order
        if waiting and waiting[0] is not status:
            return False
        # check the available connections first for matching origin and
        # availability
        for idx, connection in enumerate(self._available):
            # connections in the 'available' connection should never be active
            # they can be closed
            assert connection.state is not HttpState.ACTIVE, "attempt_to_acquire_connection: available connection in ACTIVE state"
            if connection.origin == origin and connection.is_available():
                self._available.pop(idx)
                status.set_connection(connection)
                self._busy.insert(0, connection)
                return True
        # find an idle or closed connection and close it thus freeing a connection
        # to potentially go to a different origin
        if self.num_connections >= self.max_connections:
            for idx, connection in reversed(list(enumerate(self._available))):
                if connection.state in (HttpState.IDLE, HttpState.CLOSED):
                    await connection.aclose()
                    self._available.pop(idx)
                    break
        # no connections available
        if self.num_connections >= self.max_connections:
            return False
        # open a new connection, mark it as busy
        connection = await self.open_new_connection(origin)
        status.set_connection(connection)
        self._busy.insert(0, connection)
        return True

    async def open_new_connection(self, origin: Origin) -> H11Protocol:
        connection = H11Protocol(
            origin,
            self.ssl,
            self.connect_timeout,
            self.flush_timeout,
            self.ssl_handshake_timeout,
            self.ssl_shutdown_timeout,
            self.happy_eyeballs_delay,
            self.read_buf_limit,
            self.write_buf_limit,
            self.logger,
            self.loop,
            self.auto_reconnect,
            self.max_reconnect_attempts,
            self.backoff_factor,
            self.initial_backoff,
            self.max_backoff,
            self.chunk_size,
            self.keepalive_timeout
        )
        await connection.aconnect()
        return connection

    async def response_closed(self, status: RequestStatus) -> None:
        async with self._pool_lock:
            connection: H11Protocol = status.connection
            if connection in self._busy:
                self._busy.remove(connection)
            if status in self._requests:
                self._requests.remove(status)
            # if the connection can be reused, put in the available connection
            if connection.state is not HttpState.CLOSED or connection.should_reconnect():
                self._available.insert(0, connection)
            # we might now be able to acquire a connection for a pending request
            for status in self._requests:
                if status.connection is None:
                    acquired = await self.attempt_to_acquire_connection(status)
                    if not acquired:
                        break
            # housekeeping
            self.remove_closed_connections()

    def prep_request_origin(self, request: Request) -> None:
        if not request.url.is_absolute and self.origin is not None:
            url = request.url.copy_with_origin(self.origin)
            request.url = url
        elif not request.url.is_absolute and self.origin is None:
            raise RuntimeError(
                "Cannot send request without an origin. Either provide an "
                "absolute URL or set the origin parameter on the pool"
            )

    def remove_closed_connections(self) -> None:
        for idx, connection in reversed(list(enumerate(self._available))):
            if connection.state is HttpState.CLOSED and not connection.should_reconnect():
                self._available.pop(idx)

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        await self.aclose()


@define(slots=False)
class W11Protocol(H11Mixin):
    """
    Asynchronous Websocket protocol implementation. This protocol can be used
    to open Websocket connections with hosts where the opening handshake
    occurs over the HTTP/1.1 protocol

    Parameters
    - origin (Origin): the scheme, host, port combination to establish a
    connection to
    - ssl (SSLContext): the ssl context to use for a secure connection. If
    unspecified, `ssl.create_default_context` will be used
    - close_handshake_timeout (int, float, None): the time in seconds to wait
    for the server to send the close reply frame as part of the closing handshake.
    If the timeout is exceeded, the client will close the TCP connection
    - max_buffered_messages (int): the number of messages to buffer on the protocol
    before message processing will pause. If the protocol pauses message processing
    and the server continues to send messages, TCP backpressure control will
    take over
    - ping_interval (int, float, None): the time in seconds for the client to
    wait between sending a keepalive ping
    - ping_timeout (int, float): the time in seconds to wait for a response to
    the keeepalive ping. If the timeout is exceeded the protocol will fail the
    websocket and close the connection
    - chunk_size (int): the max number of bytes to read from the transport on
    each read call
    - auto_reconnect(bool): if `True` and the peer has closed the connection, or
    a network interruption has occurred, the protocol will attempt to
    automatically re-establish a connection to the remote host
    - max_reconnect_attempts (int): if the conditions are met to attempt a
    reconnection, the protocol will attempt at most `max_reconnect_attempts` times
    before failing the protocol
    - backoff_factor (int, float): the exponential backoff delay factor to
    increment the time between reconnect attempts
    - initial_backoff (int, float): the initial time in seconds to wait after
    the first failed reconnect attempt
    - max_backoff (int, float): the max amount of time in seconds to wait for
    the next reconnect attempt
    - connect_timeout (int, float, None): the time to wait for a TCP connection
    to be established to the remote host. If `None` wait indefinitely
    - flush_timeout (int, float, None): the time in seconds to wait for the
    transport's write buffer to flush before aborting the connection
    - ssl_handshake_timeout (int, float, None): the time in seconds to wait for
    the TLS handshake to complete before aborting the connection
    - ssl_shutdown_timeout (int, float, None): the time in seconds to wait for
    the TLS closing handshake to complete before aborting the connection
    - happy_eyeballs_delay (int, float, None): the time in seconds to wait for
    a connection attempt to complete, before starting the next attempt in parallel
    - read_buf_limit (int): the low water mark limit in bytes that the protocol
    will buffer before resuming reading from the transport. The high water mark
    is 2x this limit. At which, reading from the transport will be paused
    - write_buf_limit: the high water mark limit in bytes that the transport
    will buffer before pausing writing on the protocol
    - logger (logging.Logger): logger to use on protocol
    - loop (asyncio.AbstractEventLoop): event loop to use on protocol
    """
    close_handshake_timeout: Union[int, float, None] = field(
        default=CLOSE_HANDSHAKE_TIMEOUT, validator=instance_of_or_none((int, float))
    )
    max_buffered_messages: int = field(
        default=MAX_BUFFERED_MESSAGES, validator=[instance_of(int), gt(0)]
    )
    ping_interval: Union[int, float] = field(
        default=PING_INTERVAL, validator=[instance_of((int, float)), gt(0)]
    )
    ping_timeout: Union[int, float] = field(
        default=PING_TIMEOUT, validator=instance_of((int, float))
    )
    _close_interrupt_task: asyncio.Task = field(default=None, init=False)
    _close_interrupt_waiter: asyncio.Future = field(default=None, init=False)
    _close_lock: asyncio.Lock = field(factory=asyncio.Lock, init=False)
    _data_task: asyncio.Task = field(default=None, init=False)
    _hs_auth: Auth = field(default=None, init=False)
    _hs_request: Request = field(default=None, init=False)
    _keepalive_task: asyncio.Task = field(default=None, init=False)
    _keepalive_waiter: asyncio.Future = field(default=None, init=False)
    _message: bytearray = field(factory=bytearray, init=False)
    _message_buffer: deque = field(factory=deque, init=False)
    _message_complete_waiter: asyncio.Future = field(default=None, init=False)
    _pause_waiter: asyncio.Future = field(default=None, init=False)
    _server_close: bool = field(default=False, init=False)
    _ws_close_waiter: asyncio.Future = field(default=None, init=False)
    _ws_state_machine: wsproto.connection.Connection = field(default=None, init=False)
    _ws_state: WebsocketState = field(default=WebsocketState.CLOSED, init=False)

    async def arecv(self) -> bytes:
        """
        Asynchronously receive messages from the websocket connection

        This coroutine will block until a new message is received or the connection
        is lost

        Parameters
        - None

        Returns
        - message (bytes): the next websocket message buffered on the protocol

        Raises
        - ConnectionLost: the connection is closed
        - ConnectionLostError: the connection was closed due to an error on the
        transport
        """
        if self._message_complete_waiter is not None:
            raise RuntimeError(
                "Cannot call arecv while another coroutine is waiting for data"
            )
        # if we have buffered messages we return them, even if the connection
        # is closed
        if len(self._message_buffer) > 0:
            message = self._message_buffer.popleft()
            self.maybe_resume_websocket()
            return message
        while len(self._message_buffer) == 0:
            # if the connection is closed or closing but it can reconnect, it
            # will attempt to do so. Otherwise a connection lost error will be
            # raised
            await self.ensure_open()
            waiter = self.loop.create_future()
            self._message_complete_waiter = waiter
            await waiter
            # the waiter may have finished because the connection is closed or
            # closing
            await self.ensure_open()
        message = self._message_buffer.popleft()
        self.maybe_resume_websocket()
        return message

    async def asend(
        self,
        payload: Union[AsyncIterable[Union[bytes, str]], bytes, bytearray, str, JSONType],
        timeout: Union[int, float, None] = None
    ) -> None:
        # passing an AsyncIterable that yields anything other than str or bytes
        # will raise a ValueError when we try to send it
        message = WebsocketMessage(payload)
        await self.ensure_open()
        async for event in message:
            await self.send_frame(event, timeout)

    async def ahandshake(
        self,
        request: Request,
        auth: Auth = None
    ) -> Tuple[List[wsproto.extensions.Extension], bytes]:
        """
        Asynchronously perform the opening handshake procedure to establish
        a websocket connection over the HTTP/1.1 protocol

        Parameters
        request (Request): the request to send
        auth (Auth): the auth float to be executed for this request. Defaults to
        no auth

        Returns
        - extensions (List[wsproto.extensions.Extension]): the agreed upon
        extensions to use for this connection

        Raises
        - AtEOF: EOF received from peer, could not complete response
        - ConnectionLost: the connection is closed
        - ConnectionLostError: the connection was closed due to an error on the
        transport
        - LocalProtocolError: client violated HTTP/1.1 protocol
        - RemoteProtocolError: peer violated HTTP/1.1 protocol or opening
        handshake protocol
        - ReadTimeout: timeout reached waiting for data, could not complete
        response
        - WriteTimeout: timeout reached waiting for transport buffer to flush,
        could not complete request
        - RuntimeError: client state is not IDLE or client tried to send request
        to mismatched origin
        """
        if self._ws_state is not WebsocketState.CLOSED:
            raise RuntimeError(
                f"Cannot initiate opening handshake in state {self._ws_state.name}"
            )
        key = base64.b64encode(os.urandom(16))
        request.headers['Sec-Websocket-Key'] = key
        response = await self.arequest(request, auth)
        if response.status_code != 101:
            await super().aclose()
            raise InvalidHandshake(
                request,
                response.status_code,
                response.reason_phrase
            )
        self._state = HttpState.SWITCHING
        await response.aread()
        try:
            self.establish_connection(request, response, key)
            extensions = self.client_extension_handshake(request, response)
        except RemoteProtocolError:
            await super().aclose()
            raise
        else:
            # remove the authorization header so that the auth flow can reset
            # itself in the event of a reconnect
            request.headers.remove('Authorization')
            self._hs_auth = auth
            self._hs_request = request
            self._http_state = HttpState.SWITCHED
            self._ws_state = WebsocketState.OPEN
            self._ws_state_machine = wsproto.connection.Connection(
                connection_type=wsproto.connection.ConnectionType.CLIENT,
                extensions=extensions,
                trailing_data=self._h11_state_machine.trailing_data[0]
            )
            self._data_task = self.loop.create_task(self.data_task())
            self._close_interrupt_task = self.loop.create_task(self.closer_task())
            self._keepalive_task = self.loop.create_task(self.keepalive_ping())

    async def aclose(self) -> None:
        """
        Asynchronously close the websocket connection

        This coroutine will attempt to do the closing handshake if the closing
        handshake was not already initiated by the server. It will then cleanly
        close the TCP connection

        Parameters
        - None

        Returns
        - None

        Raises
        - None
        """
        # if two coroutines call aclose concurrently we dont want one coroutine
        # closing the transport while the other is waiting for the closing
        # handshake to complete so we have a lock here
        async with self._close_lock:
            if self._ws_state in (ProtocolState.CLOSED, WebsocketState.CLOSING):
                return await super().aclose()
            self._ws_state = WebsocketState.CLOSING
            # always default to 1000 close code, the codes arent particularly
            # useful as the client plus we are in a OPEN state and actively
            # trying to close, seems like a normal close to me
            close_frame = CloseConnection(1000, WebsocketReasonPhrase.get_reason(1000))
            try:
                self.logger.debug("Closing websocket")
                await self.send_frame(close_frame, self.close_handshake_timeout)
            except WriteTimeout:
                self.logger.debug("Timed out sending close frame to server")
                return await super().aclose()
            except (ConnectionLost, ConnectionLostError):
                return
            except asyncio.CancelledError:
                return await super().aclose()
            task = self._data_task
            self._data_task = None
            if task is not None and not task.done():
                try:
                    await asyncio.wait_for(task, self.close_handshake_timeout)
                except asyncio.TimeoutError:
                    self.logger.debug("%r: Timed out waiting for close reply from server", self.origin)
                    return await super().aclose()
                except (ConnectionLost, ConnectionLostError):
                    return
                except asyncio.CancelledError:
                    return await super().aclose()
                else:
                    await super().aclose()

    async def ensure_open(self) -> None:
        if self._ws_state is WebsocketState.CLOSING:
            waiter = self.loop.create_future()
            self._ws_close_waiter = waiter
            await waiter
        # reconnect is controlled by asend/arecv methods
        if self.should_reconnect():
            await self.reconnect()
        if self._ws_state is WebsocketState.CLOSED:
            assert self._protocol_state in (ProtocolState.CLOSED, ProtocolState.CLOSING)
            self.check_closed()

    async def reconnect(self) -> None:
        connected = await super().reconnect()
        if not connected:
            raise self._exception
        await self.ahandshake(self._hs_request, self._hs_auth)
    
    async def fail_websocket(self):
        if self._ws_state in (WebsocketState.CLOSED, WebsocketState.CLOSING):
            return
        close_frame = CloseConnection(1006, WebsocketReasonPhrase.get_reason(1006))
        data = self._ws_state_machine.send(close_frame)
        self._ws_state = WebsocketState.CLOSING
        try:
            self.logger.debug("%r: Failed websocket, sending close frame", self.origin)
            self.write(data)
        except RuntimeError:
            # writing paused, transport buffer must flush but we're closing
            # and cant wait so we just abort
            self.abort()
        except (ConnectionClosing, ConnectionLost, ConnectionLostError):
            pass
        else:
            self.close()
            await self.wait_flushed()

    async def closer_task(self) -> None:
        waiter = self.loop.create_future()
        try:
            await waiter
        except asyncio.CancelledError:
            if self._ws_state is WebsocketState.OPEN:
                self.logger.debug("Failing websocket on interrupt")
                # try and send close frame before exiting
                await self.fail_websocket()
            raise

    async def data_task(self):
        frame_generator = self.receive_frame()
        try:
            while True:
                try:
                    if self._pause_waiter is not None:
                        waiter = self._pause_waiter
                        await waiter
                except asyncio.CancelledError:
                    raise
                event = await frame_generator.__anext__()
                if isinstance(event, CloseConnection):
                    return await self.handle_close_frame(event)
                elif isinstance(event, Ping):
                    await self.handle_ping(event)
                elif isinstance(event, Pong):
                    self.handle_pong()
                elif isinstance(event, Message):
                    data = event.data
                    if isinstance(data, str):
                        data = data.encode()
                    self._message.extend(data)
                    if event.message_finished:
                        self._message_buffer.append(bytes(self._message))
                        self._message.clear()
                        self.maybe_pause_websocket()
                        self.wakeup_receiver()
        finally:
            await frame_generator.aclose()

    async def keepalive_ping(self) -> None:
        if self.ping_interval is None:
            return
        while True:
            # server sent a close frame
            if self._server_close:
                return
            await asyncio.sleep(self.ping_interval)
            if self._pause_waiter is not None:
                waiter = self._pause_waiter
                await waiter
            payload = struct.pack("!I", random.getrandbits(32))
            ping_frame = Ping(payload)
            self.logger.debug("Sending keepalive ping")
            await self.send_frame(ping_frame, None)
            waiter = self.loop.create_future()
            self._keepalive_waiter = waiter
            try:
                await asyncio.wait_for(waiter, self.ping_timeout)
            except asyncio.TimeoutError:
                self.logger.debug("Timed out waiting for keepalive pong")
                await self.fail_websocket()
                break
            else:
                self.logger.debug("Received keepalive pong")

    async def send_frame(self, event: Event, timeout: Union[int, float, None]) -> None:
        try:
            self.check_closed()
        except ConnectionClosing:
            waiter = self.get_close_waiter()
            await waiter
            raise self._exception
        data = self._ws_state_machine.send(event)
        await self.awrite(data, timeout)

    async def receive_frame(self) -> AsyncGenerator[Event, None]:
        while True:
            try:
                self.check_closed()
            except ConnectionClosing:
                waiter = self.get_close_waiter()
                await waiter
                raise self._exception
            for event in self._ws_state_machine.events():
                yield event
            try:
                data = await self.aread(self.chunk_size, None)
            except AtEOF:
                await self.fail_websocket()
                break
            self._ws_state_machine.receive_data(data)
    
    async def handle_close_frame(self, event: CloseConnection) -> None:
        if self._state is not WebsocketState.OPEN:
            return
        self._server_close = True
        response = event.response()
        self._ws_state = WebsocketState.CLOSING
        await self.send_frame(response, None)
        self.close()
        # wakeup receiver so that ensure_open is called and websocket may try
        # and reconnect
        self.wakeup_receiver()
        await self.wait_flushed()

    async def handle_ping(self, event: Ping) -> None:
        response = event.response()
        await self.send_frame(response, None)

    async def __aiter__(self) -> AsyncIterable[bytes]:
        while True:
            message = await self.arecv()
            yield message

    def handle_pong(self) -> None:
        self.set_future('_keepalive_waiter')

    def maybe_pause_websocket(self):
        if self._pause_waiter is not None:
            return
        if len(self._message_buffer) > self.max_buffered_messages:
            self._pause_waiter = self.loop.create_future()
            self.logger.debug("%r: Websocket paused", self.origin)

    def maybe_resume_websocket(self):
        if self._pause_waiter is None:
            return
        if len(self._message_buffer) <= self.max_buffered_messages / 2:
            self.set_future('_pause_waiter')
            self.logger.debug("%r: Resumed websocket", self.origin)

    def wakeup_receiver(self) -> None:
        self.set_future('_message_complete_waiter')

    def connection_lost(self, exc: Union[Exception, None]) -> None:
        super().connection_lost(exc)
        self._ws_state = WebsocketState.CLOSED
        self.cancel_task('_data_task')
        self.cancel_task('_close_interrupt_task')
        self.cancel_task('_keepalive_task')
        # connection may have closed abruptly and we may be able to reconnect
        self.wakeup_receiver()
        self._ws_state_machine = None
        self._server_close = False
        self._message.clear()
        self.set_future('_ws_close_waiter')

    def establish_connection(
        self,
        request: Request,
        response: H11Response,
        key: str
    ) -> None:
        connection = response.headers.get_list('connection', split_commas=True)
        accept = response.headers.get('sec-websocket-accept').encode('ascii')
        accepted_subprotocol = response.headers.get('sec-websocket-protocol')
        upgrade = response.headers.get('upgrade')
        if not connection or not any(
            token.lower() == 'upgrade' for token in connection
        ):
            raise RemoteProtocolError("Missing header, 'Connection: Upgrade'")
        if upgrade is None or upgrade.lower() != 'websocket':
            raise RemoteProtocolError("Missing header, 'Upgrade: WebSocket'")
        accept_token = base64.b64encode(hashlib.sha1(key + ACCEPT_GUID).digest())
        if accept != accept_token:
            raise RemoteProtocolError("Bad accept token")
        if accepted_subprotocol is not None:
            client_subprotocols = request.subprotocols
            if not any(
                    client_subprotocol.lower() == accepted_subprotocol for
                    client_subprotocol in client_subprotocols
                ):
                    raise RemoteProtocolError(
                        f"Unrecognized subprotocol {accepted_subprotocol}"
                    )
    
    def client_extension_handshake(
        self,
        request: Request,
        response: H11Response
    ) -> List[wsproto.extensions.Extension]:
        accepted_extensions = []
        client_extensions = request.extensions
        server_extensions = response.headers.get_list(
            'sec-websocket-extensions',
            split_commas=True
        )
        for extension in server_extensions:
            name = extension.split(";", 1)[0].strip()
            for client_extension in client_extensions:
                if client_extension.name == name:
                    client_extension.finalize(extension)
                    accepted_extensions.append(extension)
                    break
            else:
                raise RemoteProtocolError(f"Unrecognized extension {name}")
        return accepted_extensions

    def should_reconnect(self) -> bool:
        return super().should_reconnect() and self._ws_state is WebsocketState.CLOSED

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        await self.aclose()