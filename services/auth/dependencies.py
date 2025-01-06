from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import Logger

from common.sql.orm import GetSQLDB
from common.sql.postgres_connection import PostgreSQLConnection

from common.contracts.protocols import CreateRepository, CreateService, CreateClient
from app.contracts.clients import SecurityClient
from app.contracts.repositories import ClientRepository, ClientScopeRepository
from app.contracts.services import (
    ClientService,
)

from app.adapters.output.database.repositories import (
    SQLClientRepository,
    SQLClientScopeRepository,
)
from app.infra.security import SecurityClientImpl
from app.services.client import ClientServiceImpl

from app.infra.config import Settings


class AuthDependencies:
    def __init__(self, settings: Settings, logger: Logger):
        self._settings = settings
        self._logger = logger

        self.get_sql_db: GetSQLDB
        self._init_databases()

        self.create_client_repo: CreateRepository[ClientRepository]
        self.create_scope_client_repo: CreateRepository[ClientScopeRepository]
        self._init_repositories()

        self.create_security_client: CreateClient[SecurityClient]
        self._init_clients()

        self.create_client_service: CreateService[ClientService]
        self._init_services()

    def _init_databases(self):
        self.sql_connection = PostgreSQLConnection(
            self._settings.psql_dsn, self._settings.psql_schema
        )
        self.get_sql_db = self.sql_connection.get_db

    def _init_repositories(self):
        @asynccontextmanager
        async def create_client_repo() -> AsyncGenerator[SQLClientRepository, None]:
            async with self.get_sql_db() as session:
                yield SQLClientRepository(session)

        @asynccontextmanager
        async def create_client_scope_repo() -> (
            AsyncGenerator[SQLClientScopeRepository, None]
        ):
            async with self.get_sql_db() as session:
                yield SQLClientScopeRepository(session)

        self.create_client_repo = create_client_repo
        self.create_scope_client_repo = create_client_scope_repo

    def _init_clients(self):
        @asynccontextmanager
        async def create_security_client() -> AsyncGenerator[SecurityClientImpl, None]:
            yield SecurityClientImpl(self._settings.secret)

        self.create_security_client = create_security_client

    def _init_services(self):
        @asynccontextmanager
        async def create_client_service() -> AsyncGenerator[ClientServiceImpl, None]:
            async with (
                self.create_client_repo() as client_repo,
                self.create_scope_client_repo() as client_scope_repo,
                self.create_security_client() as security_client,
            ):
                yield ClientServiceImpl(security_client, client_scope_repo, client_repo)

        self.create_client_service = create_client_service
