from common.schemas.proxy import ProxyInfoSchema
from app.contracts.services import ProxyService
from app.schemas.proxy import ProxyInfoUpdateSchema


class ProxyStateChangedEventHandler:
    def __init__(self, proxy_service: ProxyService):
        self._service = proxy_service

    async def handle(self, info: ProxyInfoSchema):
        await self._service.update(
            info.key, ProxyInfoUpdateSchema(running=info.running, uuid=info.uuid)
        )


class ProxyEngineTerminatedEventHandler:
    def __init__(self, proxy_service: ProxyService):
        self._service = proxy_service
        pass

    async def handle(self, info: ProxyInfoSchema):
        pass  # TODO: complete handle
