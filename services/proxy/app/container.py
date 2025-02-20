from logging import Logger
from dependency_injector import providers, containers

from common.containers.auth import LocalAuthContainer
from common.containers.postgres import PostgresContainer
from common.containers.rabbitmq import RabbitMQContainer, create_queue, get_exchange
from common.auth import LocalAuthService
from common.messaging.bus import MessageBus
from common.events.scope import ScopeChangedEvent
from common.messaging.clients import RabbitMQInClient
from common.containers.grpc import get_channel

from app.infra.database.uow import SQLProxyUnitOfWork
from app.infra.grpc import GRPCXrayClient
from app.services.proxy import ProxyServiceImpl


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger = providers.Dependency(Logger)

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
    message_bus = providers.Singleton(
        MessageBus, logger, client_in=scope_message_client
    )

    scope_event = providers.Singleton(ScopeChangedEvent)

    proxy_uow = providers.Factory(
        SQLProxyUnitOfWork, postgres_container.container.async_sessionmaker
    )

    xray_grpc_channel = providers.Resource(
        get_channel,
        config.ssl_certfile,
        host=config.xray_host,
        port=config.xray_port,
        logger=logger,
    )
    xray_client = providers.Singleton(GRPCXrayClient, xray_grpc_channel)

    auth_service = providers.Resource(
        LocalAuthService, auth_container.container.security_client
    )

    proxy_service = providers.Factory(ProxyServiceImpl, proxy_uow, xray_client)
