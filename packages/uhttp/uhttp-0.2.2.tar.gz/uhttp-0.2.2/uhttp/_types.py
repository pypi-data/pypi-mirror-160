import asyncio
from typing import (
    AsyncGenerator,
    AsyncIterable,
    Dict,
    Generator,
    List,
    NewType,
    Protocol,
    Union
)

from ._enums import HttpState



JSONType = Union[str, int, float, bool, List["JSONType"], Dict[str, "JSONType"]]
RequestType = NewType('RequestType', object)


class AuthType(Protocol):
    def auth_flow(
        self,
        request: RequestType
    ) -> Generator[RequestType, AsyncIterable[bytes], None]:
        ...

    async def async_auth_flow(
        self,
        request: RequestType
    ) -> AsyncGenerator[RequestType, AsyncIterable[bytes]]:
        ...


class HttpProtocolType(Protocol):
    @property
    def state(self) -> HttpState:
        ...

    @property
    def transport(self) -> Union[asyncio.Transport, None]:
        ...

    @property
    def peercert(self) -> Union[Dict[str, str], None]:
        ...

    @property
    def peercert_b(self) -> Union[bytes, None]:
        ...

    async def aclose(self) -> None:
        ...

    async def aconnect(self) -> None:
        ...

    async def arequest(
        self,
        request: RequestType,
        auth: AuthType = None
    ) -> AsyncIterable[bytes]:
        ...
    
    async def receive_response_content(
        self,
        timeout: Union[int, float, None]
    ) -> AsyncGenerator[bytes, None]:
        ...

    async def response_closed(self) -> None:
        ...


class HttpPoolType(Protocol):
    async def aclose(self) -> None:
        ...

    async def arequest(
        self,
        request: RequestType,
        auth: AuthType = None
    ) -> AsyncIterable[bytes]:
        ...

    async def response_closed(self, status: object) -> None:
        ...