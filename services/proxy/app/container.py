from logging import Logger
from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager
from dependency_injector import providers, containers
from dependency_injector.wiring import inject, Provide
from grpc import Channel

from common.containers.auth import LocalAuthContainer
from common.containers.postgres import PostgresContainer
from common.containers.rabbitmq import RabbitMQContainer, create_queue, get_exchange
from common.containers.redis import RedisContainer
from common.containers.grpc import get_channel

from common.auth import LocalAuthService
from common.messaging.bus import MessageBus
from common.events.scope import ScopeChangedEvent
from common.events.proxy import ProxyInfoChangedEvent, ProxyTerminatedEvent
from common.messaging.clients import RabbitMQInClient, RabbitMQOutClient
from common.caching.redis import RedisInClient, RedisLeaderElector

from app.contracts.clients import ProxyClientManager
from app.contracts.services import ProxyService
from app.infra.database.uow import SQLProxyUnitOfWork
from app.infra.grpc.pull import GRPCProxyClientPull, GetChannelContext
from app.services.proxy import ProxyServiceImpl
from app.infra.caching import RedisProxyCachingClient, create_egnine_keys_filter
from app.infra.events.proxy import KeyHSetEvent, KeyExpiredEvent


def generate_get_channel_context(
    with_cert=True, logger: Logger | None = None
) -> GetChannelContext:
    @asynccontextmanager
    async def get_channel_context(addr: str) -> AsyncGenerator[Channel, Any]:
        host, port = addr.split(":")
        try:
            generator = get_channel(with_cert, logger=logger, host=host, port=port)
            yield await anext(generator)
        finally:
            try:
                await anext(generator)
            except StopAsyncIteration:
                return

    return get_channel_context


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger = providers.Dependency(Logger)

    rabbit_scope_container = providers.Container(RabbitMQContainer, config=config)
    rabbit_proxy_container = providers.Container(RabbitMQContainer, config=config)
    postgres_container = providers.Container(PostgresContainer, config=config)
    auth_container = providers.Container(LocalAuthContainer, config=config)
    redis_container = providers.Container(RedisContainer, config=config)

    # Rabbit
    scope_exchange = providers.Singleton(
        get_exchange,
        rabbit_scope_container.container.channel,
        exchange_name=config.exchange_name,
    )
    proxy_exchange = providers.Singleton(
        get_exchange,
        rabbit_proxy_container.container.channel,
        exchange_name=config.exchange_name,
    )
    scope_queue = providers.Singleton(
        create_queue,
        rabbit_scope_container.container.channel,
        scope_exchange,
        queue_name=config.scope_queue_name,
        routing_key=config.scope_routing_key,
    )

    filtrate_engine_keys = providers.Singleton(
        create_egnine_keys_filter, config.engines_pattern
    )

    # Clients
    scope_message_client = providers.Singleton(
        RabbitMQInClient,
        scope_queue,
    )
    info_message_client = providers.Singleton(
        RedisInClient,
        redis_container.container.connection,
        config.engines_sub_channels,
        filtrate_engine_keys,
    )
    proxy_message_client = providers.Factory(
        RabbitMQOutClient,
        proxy_exchange,
        routing_key=config.proxy_routing_key,
    )
    proxy_caching_client = providers.Singleton(
        RedisProxyCachingClient,
        redis_container.container.connection,
        pattern=config.engines_pattern,
    )
    leader_elector_client = providers.Singleton(
        RedisLeaderElector,
        redis_container.container.connection,
        expiration=config.leadership_ttl,
    )

    # Events
    message_bus = providers.Singleton(
        MessageBus,
        logger,
        scope_message_client,
        info_message_client,
        client_out=proxy_message_client,
    )
    scope_event = providers.Singleton(ScopeChangedEvent)
    info_event = providers.Singleton(ProxyInfoChangedEvent)
    terminated_event = providers.Singleton(ProxyTerminatedEvent)
    key_hset_event = providers.Singleton(KeyHSetEvent)
    key_expired_event = providers.Singleton(KeyExpiredEvent)

    proxy_uow = providers.Factory(
        SQLProxyUnitOfWork, postgres_container.container.async_sessionmaker
    )
    get_channel_context = providers.Singleton(
        generate_get_channel_context, True, logger
    )
    engines_pull = providers.Singleton(GRPCProxyClientPull, get_channel_context)

    # Services
    auth_service = providers.Resource(
        LocalAuthService, auth_container.container.security_client
    )
    proxy_service = providers.Factory(
        ProxyServiceImpl,
        proxy_uow,
        engines_pull,
        proxy_caching_client,
        info_event,
        terminated_event,
        leader_elector_client,
    )


@asynccontextmanager
@inject
async def init_pull(
    container: Container = Provide[Container],
) -> AsyncGenerator[None, None]:
    client_pull = None
    logger = container.logger()
    try:
        proxy_service: ProxyService = await container.proxy_service()
        client_pull = container.engines_pull()

        logger.info("Pulling engines info.")
        records = await proxy_service.pull()
        logger.info("Engines info pulled.")

        if len(records) == 0:
            logger.warning("Active proxy engines not found.")

        for info in records:
            await client_pull.registrate(info)
            logger.info(f"Proxy engine [{info.key}] registrated.")
        yield
    finally:
        logger.info("Stopping proxy clients pull.")
        if client_pull is not None:
            await client_pull.clear()
        logger.info("Proxy clients pull stopped.")
