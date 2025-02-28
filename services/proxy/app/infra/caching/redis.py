from redis.asyncio import Redis

from app.contracts.clients import ProxyCachingClient
from common.schemas.proxy import ProxyInfoSchema


class RedisProxyCachingClient(ProxyCachingClient):
    def __init__(self, connection: Redis, *, pattern: str = "*:*"):
        self._conn = connection
        self._pattern = pattern

    async def _get_engine_info(self, key: str) -> ProxyInfoSchema:
        resp = await self._conn.hgetall(key)
        resp["key"] = key

        return ProxyInfoSchema.model_validate_strings(resp)

    async def get_all(self):
        result = []
        cursor = 0

        while True:
            cursor, keys = await self._conn.scan(cursor, match=self._pattern, count=100)

            for key in keys:
                info = await self._get_engine_info(key)
                result.append(info)

            if cursor == 0:
                break

        return result
