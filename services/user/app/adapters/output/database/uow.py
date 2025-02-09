from typing import Self

from common.sql.uow import SQLUnitOfWork
from app.contracts.uow import UserUnitOfWork

from app.contracts.repositories import UserRepository

from app.adapters.output.database.repositories import (
    SQLUserRepository,
)


class SQLUserUnitOfWork(SQLUnitOfWork, UserUnitOfWork):
    async def __aenter__(self) -> Self:
        uow = await super().__aenter__()
        self.user: UserRepository = SQLUserRepository(self._session)
        return uow
