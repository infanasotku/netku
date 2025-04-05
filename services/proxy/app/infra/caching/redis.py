from redis.asyncio import Redis

from app.contracts.clients import ProxyCachingClient
from app.schemas.proxy import ProxyInfoFullSchema


class RedisProxyCachingClient(ProxyCachingClient):
    def __init__(self, connection: Redis, *, pattern: str = "*:*"):
        self._conn = connection
        self._pattern = pattern

    async def get_all(self):
        result = []
        cursor = 0

        while True:
            cursor, keys = await self._conn.scan(cursor, match=self._pattern, count=100)

            for key in keys:
                info = await self.get_by_key(key)
                result.append(info)

            if cursor == 0:
                break

        return result

    async def get_by_key(self, key):
        resp = await self._conn.hgetall(key)
        if len(resp) == 0:
            return

        resp["key"] = key
        return ProxyInfoFullSchema.model_validate_strings(resp)
