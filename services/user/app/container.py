from dependency_injector import containers, providers
from common.sql.postgres_containter import PostgresContainer

from app.adapters.output.database.repositories import (
    SQLUserRepository,
)
from app.services.user import UserServiceImpl


@containers.copy(PostgresContainer)
class Container(PostgresContainer):
    user_repository = providers.Factory(SQLUserRepository, PostgresContainer.session)

    user_service = providers.Factory(UserServiceImpl, user_repository)
