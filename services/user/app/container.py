from dependency_injector import providers, containers
from common.containers.auth import LocalAuthContainer
from common.containers.postgres import PostgresContainer
from common.containers.rabbitmq import RabbitMQContainer, create_queue, get_exchange
from common.containers.utils import with_context

from app.adapters.output.database.repositories import (
    SQLUserRepository,
)
from app.services.user import UserServiceImpl
from common.messaging.clients import RabbitMQInClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    rabbit_container = providers.Container(RabbitMQContainer, config=config)
    postgres_container = providers.Container(PostgresContainer, config=config)
    auth_container = providers.Container(LocalAuthContainer, config=config)

    scope_exchange = providers.Singleton(
        get_exchange,
        rabbit_container.container.channel,
        exchange_name=config.scope_exchange_name,
    )
    scope_queue = providers.Singleton(
        create_queue,
        rabbit_container.container.channel,
        scope_exchange,
        queue_name=config.scope_queue_name,
        routing_key=config.scope_routing_key,
    )
    scope_message_client = providers.Singleton(
        RabbitMQInClient,
        scope_queue,
    )

    user_repository = providers.Factory(
        with_context(SQLUserRepository), postgres_container.container.session
    )
    user_service = providers.Factory(with_context(UserServiceImpl), user_repository)
