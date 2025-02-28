from abc import abstractmethod
from common.contracts.clients import BaseClient
from common.schemas.proxy import ProxyInfoSchema


class ProxyCachingClient(BaseClient):
    @abstractmethod
    async def get_all(self) -> list[ProxyInfoSchema]:
        """Gets info about all engines in cache."""
