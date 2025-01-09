from dependency_injector import containers, providers
from common.sql.postgres_containter import PostgresContainer

from app.adapters.output.database.repositories import (
    SQLClientRepository,
    SQLClientScopeRepository,
)
from app.adapters.output.security import SecurityClientImpl
from app.services.client import ClientServiceImpl


@containers.copy(PostgresContainer)
class Container(PostgresContainer):
    client_repository = providers.Factory(
        SQLClientRepository, PostgresContainer.session
    )
    client_scope_repository = providers.Factory(
        SQLClientScopeRepository, PostgresContainer.session
    )

    security_client = providers.Singleton(
        SecurityClientImpl, PostgresContainer.config.jwt_secret
    )

    client_service = providers.Factory(
        ClientServiceImpl, security_client, client_scope_repository, client_repository
    )
