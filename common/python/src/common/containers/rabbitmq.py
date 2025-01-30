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


async def _get_channel(
    connection: aio_pika.abc.AbstractRobustConnection,
) -> aio_pika.abc.AbstractChannel:
    return await connection.channel()


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
