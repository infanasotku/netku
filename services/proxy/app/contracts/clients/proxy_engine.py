from abc import abstractmethod
from uuid import UUID

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
    def register(self, id: str, client: ProxyEngineClient):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def get(self, id: str) -> ProxyEngineClient | None:
        pass
