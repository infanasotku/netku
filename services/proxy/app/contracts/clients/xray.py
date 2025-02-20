from abc import abstractmethod
from uuid import UUID

from common.contracts.clients import RemoteBaseClient


class XrayClient(RemoteBaseClient):
    @abstractmethod
    async def restart(self, uuid: UUID | None = None) -> UUID | None:
        """Sends request to xray service for restart.

        If `uuid` not specified - restarts xray with random uuid.

        Returns:
            New uuid, if xray restarted, `None` otherwise.
        """
