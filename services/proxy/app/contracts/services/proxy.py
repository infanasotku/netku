from abc import abstractmethod
from uuid import UUID

from common.contracts.services import BaseService

from common.schemas.proxy import ProxyInfoSchema
from app.schemas.proxy import (
    ProxyInfoCreateSchema,
    ProxyInfoUpdateSchema,
)


class ProxyService(BaseService):
    @abstractmethod
    async def create(self, proxy_create: ProxyInfoCreateSchema) -> ProxyInfoSchema:
        """Creates proxy info.
        Returns:
            Created info if it created success.
        """

    @abstractmethod
    async def delete(self, key: str):
        """Deletes proxy info by `ProxyInfoSchema.key`.
        Raises:
            ValueError: If info not exist.
        """

    @abstractmethod
    async def update(
        self,
        id: int,
        proxy_update: ProxyInfoUpdateSchema,
    ) -> ProxyInfoSchema:
        """Updates proxy info if it exist.
        Updates info in db by `id`.
        Dispatches `ProxyInfoChangedEvent`.

        Raises:
            ValueError: If info not exist.
        Returns:
            Updated info if it updated success.
        """

    @abstractmethod
    async def restart_engine(self, id: int, uuid: UUID):
        """Restarts proxy engine with new `uuid`.

        Raises:
            ValueError: If info not exist.
            RuntimeError: If xray restarted with error.
        """

    @abstractmethod
    async def pull(self):
        """Pulls info about all engines and saves it to the db."""
