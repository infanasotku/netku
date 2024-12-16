from abc import abstractmethod

from app.contracts.clients.base import InternalBaseClient


class XrayClient(InternalBaseClient):
    @abstractmethod
    async def restart(self) -> str | None:
        """Sends request to xray service for restart,
        obtains new uid.

        :return: New uid, if xray restarted, `None` otherwise.
        """
