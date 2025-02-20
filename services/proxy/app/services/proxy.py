from app.contracts.clients import ProxyClient
from app.contracts.services import ProxyService
from app.contracts.uow import ProxyUnitOfWork
from app.schemas.proxy import ProxyInfoUpdateSchema


class ProxyServiceImpl(ProxyService):
    def __init__(self, proxy_uow: ProxyUnitOfWork, xray_client: ProxyClient):
        self._proxy_uow = proxy_uow
        self._xray_client = xray_client

    async def get_proxy_info(self):
        async with self._proxy_uow as uow:
            return await uow.proxy.get_proxy_info()

    async def create_proxy_info(self, proxy_create):
        async with self._proxy_uow as uow:
            return await uow.proxy.create_proxy_info(proxy_create)

    async def update_proxy_info(self, proxy_update):
        async with self._proxy_uow as uow:
            return await uow.proxy.update_proxy_info(proxy_update)

    async def sync_with_xray(self):
        async with self._proxy_uow as uow:
            info = await uow.proxy.get_proxy_info()

            if info is None:
                raise ValueError("Proxy info not exist.")

            if info.synced_with_xray:
                raise ValueError("Info already synced.")

            xray_uuid = await self._xray_client.restart(info.uuid)
            if xray_uuid != info.uuid:
                raise RuntimeError("Xray uuid is different from the one transmitted.")

            info_update = ProxyInfoUpdateSchema(synced_with_xray=True)
            await uow.proxy.update_proxy_info(info_update)
