from typing import Any, AsyncGenerator
from dependency_injector import containers, providers
import aio_pika

from common.containers.base import BaseContainer


async def _get_connection(
    *, username: str, password: str, host: str, port: int, virtualhost: str
) -> AsyncGenerator[aio_pika.abc.AbstractRobustConnection, Any]:
    connection = await aio_pika.connect_robust(
        login=username,
        password=password,
        host=host,
        port=port,
        virtualhost=virtualhost,
    )
    yield connection
    await connection.close()


async def _get_channel(
    connection: aio_pika.abc.AbstractRobustConnection,
) -> aio_pika.abc.AbstractChannel:
    return await connection.channel()


async def get_exchange(
    channel: aio_pika.abc.AbstractChannel, *, exchange_name: str
) -> aio_pika.abc.AbstractExchange:
    return await channel.get_exchange(exchange_name)


async def create_queue(
    channel: aio_pika.abc.AbstractChannel,
    exchange: aio_pika.abc.AbstractExchange,
    *,
    queue_name: str,
    routing_key: str,
) -> aio_pika.abc.AbstractQueue:
    queue = await channel.declare_queue(
        queue_name, auto_delete=True, arguments={"x-message-ttl": 60000}
    )

    await queue.bind(exchange, routing_key)
    return queue


@containers.copy(BaseContainer)
class RabbitMQContainer(BaseContainer):
    connection = providers.Resource(
        _get_connection,
        username=BaseContainer.config.rabbit_user,
        password=BaseContainer.config.rabbit_pass,
        host=BaseContainer.config.rabbit_host,
        port=BaseContainer.config.rabbit_port,
        virtualhost=BaseContainer.config.rabbit_vhost,
    )  # Do not use with Closing marker!

    channel = providers.Singleton(_get_channel, connection)
