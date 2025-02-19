from typing import Self

from common.sql.uow import SQLUnitOfWork
from app.contracts.uow import ProxyUnitOfWork

from app.infra.database.repositories import (
    SQLProxyInfoRepository,
)


class SQLProxyUnitOfWork(SQLUnitOfWork, ProxyUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.proxy = SQLProxyInfoRepository(self._session)
        return uow
