from app.infra.events.proxy import KeyHSetEvent, KeyExpiredEvent
from app.contracts.services import ProxyService
from app.contracts.clients import ProxyClientManager
from app.infra.events.proxy import KeyEventSchema


class ProxyStateChangedEventHandler:
    def __init__(self, proxy_service: ProxyService, proxy_pull: ProxyClientManager):
        self._service = proxy_service
        self._pull = proxy_pull

    async def handle(self, payload: KeyEventSchema):
        info = await self._service.pull_by_key(
            payload.key, acquire_prefix=KeyHSetEvent.name
        )
        if self._pull.get(payload.key) is None:
            await self._pull.registrate(info)


class ProxyEngineTerminatedEventHandler:
    def __init__(self, proxy_service: ProxyService, proxy_pull: ProxyClientManager):
        self._service = proxy_service
        self._pull = proxy_pull

    async def handle(self, payload: KeyEventSchema):
        await self._service.prune_by_key(
            payload.key, acquire_prefix=KeyExpiredEvent.name
        )
        if self._pull.get(payload.key) is not None:
            await self._pull.delete(payload.key)
