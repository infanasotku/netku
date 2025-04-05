from abc import abstractmethod
from common.contracts.clients import BaseClient
from app.schemas.proxy import ProxyInfoFullSchema


class ProxyCachingClient(BaseClient):
    @abstractmethod
    async def get_all(self) -> list[ProxyInfoFullSchema]:
        """Get info about all engines in cache."""

    @abstractmethod
    async def get_by_key(self, key: str) -> ProxyInfoFullSchema | None:
        """Get info about engine in cache.
        Returns:
            Info if it exist in cache, `None` otherwise.
        """
