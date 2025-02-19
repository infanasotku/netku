from app.contracts.services import ProxyService
from app.contracts.uow import ProxyUnitOfWork


class ProxyServiceImpl(ProxyService):
    def __init__(self, proxy_uow: ProxyUnitOfWork):
        self._proxy_uow = proxy_uow

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
