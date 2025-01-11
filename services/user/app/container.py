from dependency_injector import providers, containers
from common.containers.auth import AuthContainer
from common.containers.postgres import PostgresContainer

from app.adapters.output.database.repositories import (
    SQLUserRepository,
)
from app.services.user import UserServiceImpl


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    postgres_container = providers.Container(PostgresContainer, config=config)
    auth_container = providers.Container(AuthContainer, config=config)

    user_repository = providers.Factory(
        SQLUserRepository, postgres_container.container.session
    )
    user_service = providers.Factory(UserServiceImpl, user_repository)
