from app.contracts.repositories import ProxyInfoRepository


class SQLProxyInfoRepository(ProxyInfoRepository):
    async def get_proxy_info(self):
        raise NotImplementedError

    async def create_proxy_info(self, proxy_create):
        raise NotImplementedError

    async def update_proxy_info(self, proxy_update):
        raise NotImplementedError
