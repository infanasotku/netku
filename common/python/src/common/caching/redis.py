import asyncio
from typing import Callable, Any
from redis.asyncio import Redis

from common.contracts.clients import MessageInClient, LeaderElectionClient
from common.caching.parser import Parser, KeyEventParser


class RedisInClient(MessageInClient):
    def __init__(
        self,
        connection: Redis,
        channels: list[str],
        filter: Callable[[dict[str, Any]], bool] | None,
    ):
        self._conn = connection
        self._channels = channels
        self._filter = filter
        super().__init__()

    def _get_parser(self, msg: dict) -> Parser | None:
        chan: str = msg["channel"]
        event_type = chan.split("@")[0]
        match event_type:
            case "__keyevent":
                return KeyEventParser()
            case _:
                return

    async def run(self):
        if self._handler is None:
            raise ValueError("Consumer ran without needed handler.")
        async with self._conn.pubsub() as pubsub:
            await pubsub.psubscribe(*self._channels)

            try:
                async for msg in pubsub.listen():
                    if msg["type"] == "psubscribe" or (
                        self._filter is not None and not self._filter(msg)
                    ):
                        continue

                    parser = self._get_parser(msg)
                    if parser is None:
                        continue
                    parser(msg["data"], msg["channel"])

                    await self._handler(parser.message, headers=parser.headers)

            except asyncio.CancelledError:
                await pubsub.punsubscribe()
                raise


class RedisLeaderElector(LeaderElectionClient):
    def __init__(
        self,
        connection: Redis,
        *,
        expiration: int,
    ):
        super().__init__(expiration)
        self._conn = connection

    async def try_acquire_leadership(self, acquire_id):
        lock = self._conn.lock(acquire_id, timeout=self._expiration, blocking=False)
        return await lock.acquire()
