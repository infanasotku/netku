from abc import abstractmethod
from uuid import UUID

from common.contracts.clients import RemoteBaseClient


class ProxyClient(RemoteBaseClient):
    @abstractmethod
    async def restart(self, uuid: UUID | None = None) -> UUID | None:
        """Sends request to proxy for restart.

        If `uuid` not specified - restarts proxy with random uuid.

        Returns:
            New uuid, if proxy restarted, `None` otherwise.
        """

    @abstractmethod
    async def check_engine_health(self) -> UUID | None:
        """Checks health of proxy engine.

        Returns:
            Current uuid if engine running, `None` otherwise.
        """
