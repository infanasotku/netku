from contextlib import asynccontextmanager
from logging import Logger
from typing import AsyncGenerator

from common.sql.orm import GetSQLDB
from common.sql.postgres_connection import PostgreSQLConnection
from common.contracts.protocols import CreateRepository, CreateService

from app.contracts.repositories import (
    UserRepository,
)
from app.contracts.services import (
    UserService,
)

from app.adapters.output.database.repositories import (
    SQLUserRepository,
)
from app.services.user import UserServiceImpl

from app.infra.config import Settings


class UserDependencies:
    def __init__(self, settings: Settings, logger: Logger):
        self._settings = settings
        self._logger = logger

        self.get_sql_db: GetSQLDB
        self._init_databases()

        self.create_user_repo: CreateRepository[UserRepository]
        self._init_repositories()

        self.create_user_service: CreateService[UserService]
        self._init_services()

    def _init_databases(self):
        self.sql_connection = PostgreSQLConnection(
            self._settings.psql_dsn, self._settings.psql_schema
        )
        self.get_sql_db = self.sql_connection.get_db

    def _init_repositories(self):
        @asynccontextmanager
        async def create_user_repo() -> AsyncGenerator[SQLUserRepository, None]:
            async with self.get_sql_db() as session:
                yield SQLUserRepository(session)

        self.create_user_repo = create_user_repo

    def _init_services(self):
        @asynccontextmanager
        async def create_user_service() -> AsyncGenerator[UserServiceImpl, None]:
            async with self.create_user_repo() as repo:
                yield UserServiceImpl(repo)

        self.create_user_service = create_user_service
