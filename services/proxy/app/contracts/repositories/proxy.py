from abc import abstractmethod

from common.contracts.repository import BaseRepository

from common.schemas.proxy import ProxyInfoSchema
from app.schemas.proxy import (
    ProxyInfoCreateSchema,
    ProxyInfoUpdateSchema,
)


class ProxyInfoRepository(BaseRepository):
    @abstractmethod
    async def get_by_id(self, id: int) -> ProxyInfoSchema | None:
        """Finds proxy info by `ProxyInfoSchema.id`.
        Returns:
            Proxy info if it exist in db, `None` otherwise.
        """

    @abstractmethod
    async def get_by_key(self, key: str) -> ProxyInfoSchema | None:
        """Finds proxy info by `ProxyInfoSchema.key`.
        Returns:
            Proxy info if it exist in db, `None` otherwise.
        """

    @abstractmethod
    async def create(self, proxy_create: ProxyInfoCreateSchema) -> ProxyInfoSchema:
        """Creates proxy info.
        Returns:
            Created info if it created success.
        """

    @abstractmethod
    async def update(
        self, id: int, proxy_update: ProxyInfoUpdateSchema
    ) -> ProxyInfoSchema:
        """Updates proxy info by `ProxyInfoSchema.id` if it exist in db.
        Raises:
            ValueError: If info not exist.
        Returns:
            Updated info if it updated success.
        """

    @abstractmethod
    async def delete_by_id(self, id: int):
        """Deletes proxy info by `ProxyInfoSchema.id`.
        Raises:
            ValueError: If info not exist.
        """

    @abstractmethod
    async def delete_by_key(self, key: str):
        """Deletes proxy info by `ProxyInfoSchema.key`.
        Raises:
            ValueError: If info not exist.
        """

    @abstractmethod
    async def delete_all(self):
        """Delete all records in db."""
