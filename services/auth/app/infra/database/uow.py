from typing import Self

from common.sql.uow import SQLUnitOfWork
from app.contracts.uow import ClientScopeUnitOfWork

from app.contracts.repositories import ClientRepository, ClientScopeRepository

from app.infra.database.repositories import (
    SQLClientRepository,
    SQLClientScopeRepository,
)


class SQLClientScopeUnitOfWork(SQLUnitOfWork, ClientScopeUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.client: ClientRepository = SQLClientRepository(self._session)
        self.client_scope: ClientScopeRepository = SQLClientScopeRepository(
            self._session
        )
        return uow
