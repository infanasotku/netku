from abc import abstractmethod
from uuid import UUID

from common.schemas.proxy import ProxyInfoSchema
from common.contracts.clients import RemoteBaseClient


class ProxyEngineClient(RemoteBaseClient):
    @abstractmethod
    async def restart(self, uuid: UUID | None = None) -> UUID | None:
        """Sends request to proxy for restart.

        If `uuid` not specified - restarts proxy with random uuid.

        Returns:
            New uuid, if proxy restarted, `None` otherwise.
        """


class ProxyClientPull:
    @abstractmethod
    def get(self, key: str) -> ProxyEngineClient | None:
        pass


class ProxyClientManager(ProxyClientPull):
    @abstractmethod
    async def registrate(self, info: ProxyInfoSchema):
        """Regisrates proxy client by `info`."""

    @abstractmethod
    async def clear(self):
        """Clears and turns off all proxy client."""

    @abstractmethod
    async def delete(self, key: str):
        """Deletes and turns off proxy client by `key`."""
