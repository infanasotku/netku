from dependency_injector import containers, providers
from common.containers.postgres import PostgresContainer

from app.adapters.output.database.repositories import (
    SQLClientRepository,
    SQLClientScopeRepository,
)
from app.adapters.output.security import SecurityClientImpl
from app.services.client import ClientServiceImpl


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    postgres_container = providers.Container(PostgresContainer, config=config)

    client_repository = providers.Factory(
        SQLClientRepository, postgres_container.container.session
    )
    client_scope_repository = providers.Factory(
        SQLClientScopeRepository, postgres_container.container.session
    )

    security_client = providers.Singleton(SecurityClientImpl, config.jwt_secret)

    client_service = providers.Factory(
        ClientServiceImpl, security_client, client_scope_repository, client_repository
    )
