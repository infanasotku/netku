from dependency_injector import providers, containers
from common.containers.auth import LocalAuthContainer
from common.containers.postgres import PostgresContainer
from common.containers.utils import with_context

from app.adapters.output.database.repositories import (
    SQLUserRepository,
)
from app.services.user import UserServiceImpl


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    postgres_container = providers.Container(PostgresContainer, config=config)
    auth_container = providers.Container(LocalAuthContainer, config=config)

    user_repository = providers.Factory(
        with_context(SQLUserRepository), postgres_container.container.session
    )
    user_service = providers.Factory(with_context(UserServiceImpl), user_repository)
