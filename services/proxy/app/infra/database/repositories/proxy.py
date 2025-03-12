from sqlalchemy import delete, select
from sqlalchemy.orm import InstrumentedAttribute

from common.sql.repository import SQLBaseRepository
from app.contracts.repositories import ProxyInfoRepository
from app.infra.database.models import ProxyInfo

from app.infra.database import converters


class SQLProxyInfoRepository(ProxyInfoRepository, SQLBaseRepository):
    async def _get_by(self, column: InstrumentedAttribute, value) -> ProxyInfo | None:
        s = select(ProxyInfo).filter(column == value)

        info = (await self._session.execute(s)).scalars().first()
        return info

    async def _delete_by(self, column: InstrumentedAttribute, value):
        info = await self._get_by(column, value)

        if info is None:
            raise ValueError(f"Info with {value} not exist.")

        d = delete(ProxyInfo).filter(column == value)

        await self._session.execute(d)
        await self._session.flush()

    async def get_by_id(self, id):
        info = await self._get_by(ProxyInfo.id, id)
        if info is None:
            return None
        return converters.proxy_to_proxy_info_schema(info)

    async def get_by_key(self, key):
        info = await self._get_by(ProxyInfo.key, key)
        if info is None:
            return None
        return converters.proxy_to_proxy_info_schema(info)

    async def create(self, proxy_create):
        info = converters.proxy_create_schema_to_proxy_info(proxy_create)
        self._session.add(info)
        await self._session.flush()
        await self._session.refresh(info)

        return converters.proxy_to_proxy_info_schema(info)

    async def update(self, id, proxy_update):
        info = await self._get_by(ProxyInfo.id, id)

        if info is None:
            raise ValueError(f"Info with id {id} not exist.")

        for field in ["running"]:
            setattr(info, field, getattr(proxy_update, field))

        for field, value in proxy_update.model_dump(exclude_unset=True).items():
            setattr(info, field, value)

        await self._session.flush()
        await self._session.refresh(info)

        return converters.proxy_to_proxy_info_schema(info)

    async def delete_by_id(self, id):
        await self._delete_by(ProxyInfo.id, id)

    async def delete_by_key(self, key):
        await self._delete_by(ProxyInfo.key, key)

    async def delete_all(self):
        d = delete(ProxyInfo)

        await self._session.execute(d)
        await self._session.flush()
