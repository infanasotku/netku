from sqlalchemy import select

from common.sql.repository import SQLBaseRepository
from app.contracts.repositories import ProxyInfoRepository
from app.infra.database.models import ProxyInfo

from app.infra.database import converters


class SQLProxyInfoRepository(ProxyInfoRepository, SQLBaseRepository):
    async def get_proxy_info(self):
        s = select(ProxyInfo)

        info = (await self._session.execute(s)).scalars().first()

        if info is None:
            return None

        return converters.proxy_to_proxy_info_schema(info)

    async def create_proxy_info(self, proxy_create):
        old_info = await self.get_proxy_info()
        if old_info is not None:
            raise ValueError("Proxy info already exist.")

        info = converters.proxy_create_schema_to_proxy_info(proxy_create)
        self._session.add(info)
        await self._session.flush()
        await self._session.refresh(info)

        return converters.proxy_to_proxy_info_schema(info)

    async def update_proxy_info(self, proxy_update):
        s = select(ProxyInfo)
        info = (await self._session.execute(s)).scalars().first()

        if info is None:
            raise ValueError("Proxy info not exist.")

        for field, value in proxy_update.model_dump(exclude_unset=True).items():
            setattr(info, field, value)

        await self._session.flush()
        await self._session.refresh(info)

        return converters.proxy_to_proxy_info_schema(info)
