from typing import Any, AsyncGenerator
from dependency_injector import containers, providers
from redis.asyncio import Redis

from common.containers.base import BaseContainer


async def _get_connection(
    *, host: str, port: int, password: str | None = None
) -> AsyncGenerator[Redis, Any]:
    conn = Redis(host=host, port=port, password=password)
    await conn.initialize()

    yield conn
    await conn.aclose()


@containers.copy(BaseContainer)
class RedisContainer(BaseContainer):
    connection = providers.Resource(
        _get_connection,
        host=BaseContainer.config.redis_host,
        port=BaseContainer.config.redis_port,
        password=BaseContainer.config.redis_pass,
    )  # Do not use with Closing marker!
