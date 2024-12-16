from contextlib import asynccontextmanager
from typing import AsyncGenerator, Type, TypeVar

from app.infra.database.sql_db.orm import GetSQLDB
from app.infra.database.sql_db.repositories.base import SQLBaseRepository


class SQLRepositoryFactory:
    SQLRepositoryT = TypeVar("SQLRepositoryT", bound=SQLBaseRepository)

    def __init__(
        self,
        get_db: GetSQLDB,
        repository_type: Type[SQLRepositoryT],
    ):
        self.get_db = get_db
        self._Repo = repository_type

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[SQLRepositoryT, None]:
        async with self.get_db() as session:
            yield self._Repo(session)
