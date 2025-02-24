from common.events.proxy import ProxyUUIDChangedEvent
from common.schemas.proxy import ProxyInfo

from app.contracts.clients import ProxyClient
from app.contracts.services import ProxyService
from app.contracts.uow import ProxyUnitOfWork
from app.schemas.proxy import ProxyInfoUpdateSchema


class ProxyServiceImpl(ProxyService):
    def __init__(
        self,
        proxy_uow: ProxyUnitOfWork,
        xray_client: ProxyClient,
        uuid_event: ProxyUUIDChangedEvent,
    ):
        self._proxy_uow = proxy_uow
        self._xray_client = xray_client
        self._uuid_event = uuid_event

    async def get_proxy_info(self):
        async with self._proxy_uow as uow:
            return await uow.proxy.get_proxy_info()

    async def create_proxy_info(self, proxy_create):
        async with self._proxy_uow as uow:
            return await uow.proxy.create_proxy_info(proxy_create)

    async def update_proxy_info(self, proxy_update):
        async with self._proxy_uow as uow:
            return await uow.proxy.update_proxy_info(proxy_update)

    async def sync_with_proxy(self):
        async with self._proxy_uow as uow:
            info = await uow.proxy.get_proxy_info()

            if info is None:
                raise ValueError("Proxy info not exist.")

            if info.synced:
                raise ValueError("Info already synced.")

            xray_uuid = await self._xray_client.restart(info.uuid)
            if xray_uuid != info.uuid:
                raise RuntimeError("Xray uuid is different from the one transmitted.")

            info_update = ProxyInfoUpdateSchema(synced=True, running=True)
            await uow.proxy.update_proxy_info(info_update)

            await self._uuid_event.dispatch(ProxyInfo(uuid=info.uuid))

    async def pull_from_proxy(self):
        async with self._proxy_uow as uow:
            engine_info = await self._xray_client.get_engine_info()

            info_update = await uow.proxy.get_proxy_info()

            if info_update is None:
                info_update = ProxyInfoUpdateSchema()

            if engine_info.uuid is not None:
                info_update.uuid = engine_info.uuid
                info_update.synced = True
            else:
                info_update.synced = False
            info_update.running = engine_info.running
            await uow.proxy.update_proxy_info(info_update)
