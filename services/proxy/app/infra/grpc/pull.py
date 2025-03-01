from typing import Protocol, AsyncContextManager

from grpc import Channel

from common.schemas.proxy import ProxyInfoSchema
from app.contracts.clients import ProxyEngineClient, ProxyClientManager
from app.infra.grpc.xray import GRPCXrayClient


class GetChannelContext(Protocol):
    async def __call__(self, addr: str) -> AsyncContextManager[Channel]: ...


class GRPCProxyClientPull(ProxyClientManager):
    def __init__(self, get_channel_context: GetChannelContext):
        self._pull: dict[str, ProxyEngineClient] = {}
        self._contexts: dict[str, AsyncContextManager[Channel]] = {}
        self._get_channel_context = get_channel_context

    async def registrate(self, info: ProxyInfoSchema):
        if info.key in self._pull:
            raise KeyError(f"Client {info.key} already exists in pull.")

        self._contexts[info.key] = self._get_channel_context(info.addr)
        channel = await self._contexts[info.key].__aenter__()
        self._pull[info.key] = GRPCXrayClient(channel)

    async def delete(self, key):
        del self._pull[key]
        await self._contexts[key].__aexit__()
        del self._contexts[key]

    async def clear(self):
        for key in self._contexts:
            await self._contexts[key].__aexit__(None, None, None)

        self._pull.clear()
        self._contexts.clear()

    def get(self, id: str) -> ProxyEngineClient:
        return self._pull[id]
