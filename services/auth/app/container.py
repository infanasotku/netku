from dependency_injector import containers, providers

from common.containers.postgres import PostgresContainer
from common.containers.rabbitmq import RabbitMQContainer, get_exchange
from common.containers.utils import with_context

from app.adapters.output.database.repositories import (
    SQLClientRepository,
    SQLClientScopeRepository,
)
from common.auth import PyJWTSecurityClient
from app.services.client import ClientServiceImpl
from common.messaging.clients import RabbitMQOutClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    rabbit_container = providers.Container(RabbitMQContainer, config=config)
    postgres_container = providers.Container(PostgresContainer, config=config)

    client_repository = providers.Factory(
        with_context(SQLClientRepository), postgres_container.container.session
    )
    client_scope_repository = providers.Factory(
        with_context(SQLClientScopeRepository), postgres_container.container.session
    )

    security_client = providers.Singleton(
        PyJWTSecurityClient, config.public_key, config.private_key
    )

    scope_exchange = providers.Singleton(
        get_exchange,
        rabbit_container.container.channel,
        exchange_name=config.scope_exchange_name,
    )
    scope_message_client = providers.Factory(
        RabbitMQOutClient,
        scope_exchange,
        routing_key=config.scope_routing_key,
    )
    client_service = providers.Factory(
        with_context(ClientServiceImpl),
        security_client,
        client_scope_repository,
        client_repository,
        scope_message_client,
    )
