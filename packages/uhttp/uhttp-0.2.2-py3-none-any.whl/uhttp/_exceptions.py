from typing import Union
from ._types import RequestType



class UHttpException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ReasonError(UHttpException):
    def __init__(self, exc: BaseException) -> None:
        self.reason = exc
        self.__cause__ = exc


class ConnectionLostError(ReasonError):
    pass


class ConnectionFailed(ReasonError):
    pass


class SignalError(UHttpException):
    def __init__(self) -> None:
        pass


class ConnectionLost(SignalError):
    pass


class ConnectionClosing(SignalError):
    pass


class AtEOF(SignalError):
    pass


class StreamConsumed(SignalError):
    pass


class TimeoutException(UHttpException):
    def __init__(self, timeout: Union[int, float]) -> None:
        self.timeout = timeout


class ConnectTimeout(TimeoutException):
    def __str__(self) -> str:
        return (
            f"Failed to connect in {self.timeout} second"
            f"{'s' if self.timeout != 1 else ''}"
        )


class ConnectionAcquireTimeout(TimeoutException):
    def __str__(self) -> str:
        return (
            f"Failed to acquire connection in {self.timeout} second"
            f"{'s' if self.timeout != 1 else ''}"
        )


class ReadTimeout(TimeoutException):
    def __str__(self) -> str:
        return (
            f"Failed to read data in {self.timeout} second"
            f"{'s' if self.timeout != 1 else ''}"
        )


class WriteTimeout(TimeoutException):
    def __str__(self) -> str:
        return (
            f"Failed to write data in {self.timeout} second"
            f"{'s' if self.timeout != 1 else ''}"
        )


class ProtocolError(UHttpException):
    def __init__(self, msg: str) -> None:
        if type(self) is ProtocolError:
            raise TypeError("Tried to directly instantiate ProtocolError")
        super().__init__(msg)


class RemoteProtocolError(ProtocolError):
    pass


class LocalProtocolError(ProtocolError):
    pass


class HttpStatusError(UHttpException):

    def __init__(
        self,
        request: RequestType,
        status_code: int,
        reason_phrase: str
    ) -> None:
        self._request = request
        self._status_code = status_code
        self._reason_phrase = reason_phrase

    @property
    def request(self) -> RequestType:
        return self._request

    def __str__(self) -> str:
        error_types = {
            1: "Informational response",
            3: "Redirect response",
            4: "Client error",
            5: "Server error",
        }
        status_class = self._status_code // 100
        error_type = error_types.get(status_class, 'Invalid status code')
        return (
            f"{error_type} {self._status_code} {self._reason_phrase} for "
            f"{self.request.url.target}"    # type: ignore
        )


class InvalidHandshake(HttpStatusError):
    pass