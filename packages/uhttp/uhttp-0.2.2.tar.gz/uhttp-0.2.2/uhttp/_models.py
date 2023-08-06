import asyncio
from collections import deque
import collections.abc
import json
import re
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterable,
    Dict,
    Generator,
    List,
    Sequence,
    Tuple,
    Union
)

import h11
import rfc3986
import wsproto.events
import wsproto.extensions
from attrs import define, field, frozen
from attrs import NOTHING as UseExisting
from attrs.validators import deep_iterable, instance_of
from uhttp import _package_name, _package_version

from ._enums import HttpMethod, HttpReasonPhrase
from ._exceptions import (
    AtEOF,
    ConnectionLost,
    ConnectionLostError,
    HttpStatusError,
    RemoteProtocolError,
    ReadTimeout,
    StreamConsumed
)
from ._types import HttpPoolType, HttpProtocolType, JSONType
from ._util import instance_of_or_none



HTTP_SCHEMES = {'http', 'https'}
READ_TIMEOUT = 5
SECURE_SCHEMES = {'https', 'wss'}
USER_AGENT = f"{_package_name}/{_package_version}"
VALID_SCHEMES = {'http', 'https', 'ws', 'wss'}
WEBSOCKET_SCHEMES = {'ws', 'wss'}
WEBSOCKET_VERSION = 13
WRITE_TIMEOUT = 5

content_length_re = re.compile(rb"[0-9]+")


def encode_key(key: Union[str, bytes]) -> bytes:
    if isinstance(key, (str, bytes)):
        if isinstance(key, str):
            return key.lower().strip().replace(' ', '-').encode('ascii')
        else:
            return key.lower().strip().replace(b' ', b'-')
    return key


def encode_val(val: Union[str, int, bytes]) -> bytes:
    if isinstance(val, str):
        return val.encode('ascii')
    elif isinstance(val, int):
        return str(val).encode('ascii')
    return val


def encode_headers(
    headers: Union[
        "Headers",
        Dict[str, str],
        Sequence[Tuple[str, str]],
        Sequence[Tuple[bytes, bytes]],
        Sequence["Header"]
    ]
) -> List["Header"]:
    if isinstance(headers, Headers):
        return headers.headers
    elif isinstance(headers, dict):
        return [Header(key, val) for key, val in headers.items()]
    elif isinstance(headers, collections.abc.Iterable):
        ret = []
        for item in headers:
            if isinstance(item, tuple):
                if len(item) != 2:
                    raise ValueError("Sequences of tuples must have len 2")
                ret.append(Header(item[0], item[1]))
            elif isinstance(item, Header):
                ret.append(item)
            else:
                raise TypeError("Sequence elements must be tuple or Header")
        return ret
    else:
        raise TypeError(
            "'headers' must be type "
            "Headers | Dict[str, str] | Sequence[Tuple[str, str]]]. "
            f"Got {type(headers)}"
        )


def encode_url(url: Union["URL", str, rfc3986.URIReference]) -> rfc3986.URIReference:
    if isinstance(url, str):
        return rfc3986.iri_reference(url, encoding='ascii').encode()
    elif isinstance(url, URL):
        return url.url
    else:
        return url


def encode_method(method: Union[str, HttpMethod]) -> HttpMethod:
    if isinstance(method, str):
        return HttpMethod.get_method(method)
    return method


def encode_content(
    content: Union[AsyncIterable[bytes], bytes, bytearray, str, JSONType, None]
) -> AsyncIterable[bytes]:
    if content is None:
        return
    elif isinstance(content, bytes):
        return ByteStream(content)
    elif isinstance(content, bytearray):
        return ByteStream(bytes(content))
    elif isinstance(content, str):
        return ByteStream(content.encode())
    elif isinstance(content, dict):
        return ByteStream(json.dumps(content).encode())
    else:
        return content


def default_timeouts(
    timeouts: Union[Dict[str, Union[float, int]], None]
) -> Dict[str, Union[float, int]]:
    if timeouts is None:
        return dict(read=READ_TIMEOUT, write=WRITE_TIMEOUT)
    return timeouts


@frozen
class Header:
    key: Union[str, bytes] = field(
        converter=encode_key, validator=instance_of(bytes)
    )
    val: Union[str, int, bytes] = field(
        converter=encode_val, validator=instance_of(bytes)
    )


@define
class Headers:
    headers: Union[
        "Headers",
        Dict[str, str],
        Sequence[Tuple[str, str]],
        Sequence[Tuple[bytes, bytes]],
        Sequence["Header"]
    ] = field(converter=encode_headers)

    @property
    def raw(self) -> List[Tuple[bytes, bytes]]:
        return [(header.key, header.val) for header in self.headers]

    @classmethod
    def default_headers(cls) -> "Headers":
        return cls({'User-Agent': USER_AGENT})

    def get(self, __key: str, __default: Any = None) -> str:
        try:
            return self[__key]
        except KeyError:
            return __default

    def get_list(self, __key: str, split_commas: bool = True) -> List[str]:
        key = encode_key(__key)
        found: List[str] = []
        headers: List[Header] = self.headers
        for header in headers:
            if header.key == key:
                found.append(header.val.decode('ascii'))
        if not split_commas:
            return found
        split_values = []
        for value in found:
            split_values.extend([item.strip() for item in value.split(',')])
        return split_values

    def add(self, __key: str, __val: Union[str, int]) -> None:
        new_header = Header(__key, __val)
        updated_headers = list(self.headers)
        updated_headers.append(new_header)
        self.headers = updated_headers

    def remove(self, __key: str) -> None:
        key = encode_key(__key)
        updated_headers = [
            header for header in self.headers if header.key != key
        ]
        self.headers = updated_headers

    def __getitem__(self, __key: str) -> str:
        key = encode_key(__key)
        found = []
        for header in self.headers:
            if header.key == key:
                found.append(header.val.decode('ascii'))
        if not found:
            raise KeyError(__key)
        return ', '.join(found)
    
    def __setitem__(self, __key: str, __val: str | int) -> None:
        new_header = Header(__key, __val)
        key = new_header.key
        updated_headers = [
            header for header in self.headers if header.key != key
        ]
        updated_headers.append(new_header)
        self.headers = updated_headers


@define
class Origin:
    scheme: str = field(validator=instance_of(str))
    host: str = field(validator=instance_of(str))
    port: int | None = field(default=None, validator=instance_of_or_none(int))

    @property
    def is_secure(self) -> bool:
        return self.scheme in SECURE_SCHEMES

    @scheme.validator
    def _validate_scheme(self, _, scheme: str) -> None:
        check_scheme = scheme.lower()
        if check_scheme not in VALID_SCHEMES:
            raise ValueError(f"Invalid scheme {scheme}")

    @port.validator
    def _default_port(self, _, port: int | None) -> None:
        if port is None:
            self.port = 443 if self.scheme in SECURE_SCHEMES else 80
    
    def __repr__(self) -> str:
        return f"{self.scheme}://{self.host}:{self.port}"


@define
class URL:
    url: Union["URL", str, rfc3986.URIReference] = field(
        converter=encode_url, validator=[instance_of(rfc3986.URIReference)]
    )
    _origin: Origin = field(default=None, init=False)
    
    @url.validator
    def _no_userinfo(self, _, url: rfc3986.URIReference) -> None:
        userinfo = url.authority_info().get('userinfo')
        if userinfo is not None:
            raise ValueError("URL cannot contain user info")
    
    @url.validator
    def _has_path(self, _, url: rfc3986.URIReference) -> None:
        path = url.path
        if not path:
            raise ValueError("URL must contain a valid path")

    @property
    def scheme(self) -> str:
        return self.url.scheme

    @property
    def host(self) -> str:
        return self.url.host
    
    @property
    def port(self) -> int:
        try:
            return int(self.url.port)
        except (TypeError, ValueError):
            return self.url.port

    @property
    def path(self) -> str:
        return self.url.path

    @property
    def query(self) -> str:
        return self.url.query

    @property
    def fragment(self) -> str:
        return self.url.fragment

    @property
    def target(self) -> str:
        target = self.path
        if not target.startswith('/'):
            target = '/' + target
        query = self.query
        if query is not None:
            target += f"?{query}"
        return target

    @property
    def is_absolute(self) -> bool:
        return self.url.is_absolute()

    @property
    def is_http(self) -> bool:
        scheme = self.scheme
        if scheme is not None:
            return scheme.lower() in HTTP_SCHEMES
        # relative or websocket url
        return False

    @property
    def is_websocket(self) -> bool:
        scheme = self.scheme
        if scheme is not None:
            return scheme.lower() in WEBSOCKET_SCHEMES
        # relative or http url
        return False

    @property
    def origin(self) -> Origin:
        if self.is_absolute:
            if self._origin is not None:
                return self._origin
            scheme = self.scheme
            host = self.host
            port = self.port
            origin = Origin(scheme, host, port)
            self._origin = origin
            return origin

    def copy_with(
        self,
        scheme: str = UseExisting,
        authority: str = UseExisting,
        path: str = UseExisting,
        query: str = UseExisting,
        fragment: str = UseExisting
    ) -> "URL":
        kwargs = dict(
            scheme=scheme,
            authority=authority,
            path=path,
            query=query,
            fragment=fragment
        )
        copy_with = {key: val for key, val in kwargs.items() if val is not UseExisting}
        url = self.url.copy_with(**copy_with)
        return URL(url)

    def copy_with_origin(self, origin: Origin) -> "URL":
        return self.copy_with(
            scheme=origin.scheme,
            authority=f"{origin.host}:{origin.port}"
        )

    def __repr__(self) -> str:
        return repr(self.url)


@define
class ByteStream:
    data: bytes

    @property
    def content_length(self) -> int:
        return len(self.data)

    async def __aiter__(self):
        yield self.data


@define
class WebsocketMessage:
    payload: Union[AsyncIterable[bytes], bytes, bytearray, str, JSONType] = field(
        converter=encode_content, validator=instance_of(collections.abc.AsyncIterable)
    )

    async def __aiter__(self) -> AsyncIterable[wsproto.events.Message]:
        buffer = deque()
        async for chunk in self.payload:
            buffer.append(chunk)
            if len(buffer) > 1:
                event = wsproto.events.Message(
                    data=buffer.popleft(),
                    message_finished=False
                )
                yield event
        while len(buffer) > 1:
            event = wsproto.events.Message(
                data=buffer.popleft(),
                message_finished=False
            )
            yield event
        assert len(buffer) == 1
        event = wsproto.events.Message(
            data=buffer.popleft(),
            message_finished=True
        )
        yield event

@define
class Request:
    method: Union[str, HttpMethod] = field(
        converter=encode_method, validator=instance_of((HttpMethod, str))
    )
    url: Union[URL, str, rfc3986.URIReference] = field(converter=URL)
    headers: Union[Headers, Dict[str, str], Sequence[Tuple[str, str]]] = field(
        factory=Headers.default_headers, converter=Headers
    )
    content: Union[AsyncIterable[bytes], bytes, bytearray, str, JSONType, None] = field(
        default=None,
        converter=encode_content,
        validator=instance_of_or_none(collections.abc.AsyncIterable)
    )
    timeouts: Dict[str, Union[float, int]] = field(
        default=None, converter=default_timeouts, validator=instance_of(dict)
    )
    extensions: Sequence[wsproto.extensions.Extension] = field(
        factory=list, validator=deep_iterable(wsproto.extensions.Extension)
    )
    subprotocols: Sequence[str] = field(
        factory=list, validator=deep_iterable(str)
    )

    def __attrs_post_init__(self) -> None:
        if self.url.is_absolute:
            self.headers['Host'] = self.url.host

    def to_event(self) -> h11.Request:
        if self.url.is_http:
            self._to_event_http()
        elif self.url.is_websocket:
            self._to_event_websocket()
        else:
            raise ValueError("URL must be an absolute HTTP or Websocket URL")
        return h11.Request(
            method=self.method.value,
            target=self.url.target,
            headers=self.headers.raw
        )

    def _to_event_websocket(self) -> h11.Request:
        if self.subprotocols is not None:
            subprotocol_header = ', '.join(self.subprotocols)
            self.headers['Sec-Websocket-Protocol'] = subprotocol_header
        if self.extensions is not None:
            offers: Dict[str, Union[str, bool]] = {}
            for extension in self.extensions:
                offers[extension.name] = extension.offer()
            client_extensions = []
            for name, params in offers.items():
                if isinstance(params, bool):
                    if params:
                        client_extensions.append(name)
                else:
                    client_extensions.append(b"%s; %s" % (name, params))
            if client_extensions:
                extensions_header = ', '.join(client_extensions)
                self.headers['Sec-Websocket-Extensions'] = extensions_header
        self.headers['Upgrade'] = 'websocket'
        self.headers['Connection'] = 'upgrade'
        self.headers['Sec-Websocket-Version'] = WEBSOCKET_VERSION

    def _to_event_http(self) -> h11.Request:
        if isinstance(self.content, ByteStream):
            self.headers['Content-Length'] = self.content.content_length
        elif self.content is not None:
            self.headers['Transfer-Encoding'] = 'chunked'


@define
class RequestStatus:
    request: Request
    connection: HttpProtocolType = field(default=None, init=False)
    connection_acquired: asyncio.Event = field(factory=asyncio.Event, init=False)

    def set_connection(self, connection: HttpProtocolType) -> None:
        assert self.connection is None
        self.connection = connection
        self.connection_acquired.set()

    def unset_connection(self) -> None:
        assert self.connection is not None
        self.connection = None
        self.connection_acquired.clear()

    async def wait_for_connection(self) -> HttpProtocolType:
        await self.connection_acquired.wait()
        assert self.connection is not None
        return self.connection


@define
class H11Response:
    request: Request
    event: Union[h11.Response, h11.InformationalResponse]
    connection: HttpProtocolType
    _headers: Headers = field(default=None, init=False)
    _stream_consumed: bool = field(default=False, init=False)

    @property
    def status_code(self) -> int:
        return self.event.status_code

    @property
    def headers(self) -> Headers:
        if self._headers is None:
            headers = Headers(self.event.headers.raw_items())
            self._headers = headers
        return self._headers
    
    @property
    def http_version(self) -> str:
        return self.event.http_version.decode('ascii')
    
    @property
    def is_informational(self) -> bool:
        return 100 <= self.status_code <= 199

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code <= 299

    @property
    def is_redirect(self) -> bool:
        return 300 <= self.status_code <= 399

    @property
    def is_client_error(self) -> bool:
        return 400 <= self.status_code <= 499

    @property
    def is_server_error(self) -> bool:
        return 500 <= self.status_code <= 599

    @property
    def reason_phrase(self) -> str:
        return HttpReasonPhrase.get_reason(self.status_code)

    @property
    def stream_consumed(self) -> bool:
        return self._stream_consumed
    
    def raise_for_status(self):
        if not self.is_success:
            raise HttpStatusError(
                self.request,
                self.status_code,
                self.reason_phrase
            )

    async def aclose(self) -> None:
        if not self._stream_consumed:
            self._stream_consumed = True
            await self.connection.aclose()
    
    async def aread(self) -> bytes:
        return b''.join([chunk async for chunk in self])

    async def __aiter__(self) -> AsyncIterable[bytes]:
        if self._stream_consumed:
            raise StreamConsumed()
        timeout = self.request.timeouts.get('read')
        try:
            async for chunk in self.connection.receive_response_content(timeout):
                yield chunk
        except (
            AtEOF,
            ConnectionLost,
            ConnectionLostError,
            ReadTimeout,
            RemoteProtocolError
        ):
            await self.connection.aclose()
            raise
        else:
            await self.connection.response_closed()
        finally:
            self._stream_consumed = True


@define
class H11PoolResponse:
    status: RequestStatus
    pool: HttpPoolType
    h11_response: H11Response

    async def aclose(self) -> None:
        await self.h11_response.aclose()
        await self.pool.response_closed(self.status)

    async def aread(self) -> bytes:
        try:
            return await self.h11_response.aread()
        finally:
            await self.aclose()

    async def __aiter__(self) -> AsyncIterable[bytes]:
        try:
            async for chunk in self.h11_response:
                yield chunk
        finally:
            await self.aclose()


@define(slots=False)
class Auth:
    connection: HttpProtocolType = field(default=None, init=False)

    def set_connection(self, connection: HttpProtocolType) -> None:
        self.connection = connection

    def auth_flow(self, request: Request) -> Generator[Request, H11Response, None]:
        yield request

    async def async_auth_flow(
        self,
        request: Request
    ) -> AsyncGenerator[Request, H11Response]:
        flow = self.auth_flow(request)
        request = next(flow)

        while True:
            response = yield request
            try:
                request = flow.send(response)
            except StopIteration:
                break