from abc import abstractmethod

from common.contracts.clients.base import BaseClient


class RemoteBaseClient(BaseClient):
    @abstractmethod
    async def check_health(self) -> bool:
        """Checks of remote service.

        Returns:
            `True` if service available, `False` otherwise.
        """
