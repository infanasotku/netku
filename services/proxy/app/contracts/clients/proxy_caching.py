from abc import abstractmethod
from common.contracts.clients import BaseClient
from common.schemas.proxy import ProxyInfoSchema


class ProxyCachingClient(BaseClient):
    @abstractmethod
    async def get_all(self) -> list[ProxyInfoSchema]:
        """Get info about all engines in cache."""

    @abstractmethod
    async def get_by_key(self, key: str) -> ProxyInfoSchema | None:
        """Get info about engine in cache.
        Returns:
            Info if it exist in cache, `None` otherwise.
        """
