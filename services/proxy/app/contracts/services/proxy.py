from abc import abstractmethod
from uuid import UUID

from common.contracts.services import BaseService

from common.schemas.proxy import ProxyInfoSchema


class ProxyService(BaseService):
    @abstractmethod
    async def get_by_id(self, id: int) -> ProxyInfoSchema | None:
        """Finds proxy info by `ProxyInfoSchema.id`.
        Returns:
            Proxy info if it exist in db, `None` otherwise.
        """

    @abstractmethod
    async def pull_by_key(
        self,
        key: str,
    ) -> ProxyInfoSchema:
        """
        - Pull proxy info from cache by `key`.
        - Update info in db by `key`.
        - Cause `ProxyInfoChangedEvent`.

        Raises:
            KeyError: If info not exist.
        Returns:
            Updated info if it updated success.
        """

    @abstractmethod
    async def restart_engine(self, id: int, uuid: UUID):
        """Restart proxy engine with new `uuid`.

        Raises:
            KeyError: If info not exist.
            RuntimeError: If xray restarted with error.
        """

    @abstractmethod
    async def pull(self) -> list[ProxyInfoSchema]:
        """Pull info about all engines from cache
        and saves it to the db.

        Returns:
            Pulled info.
        """
