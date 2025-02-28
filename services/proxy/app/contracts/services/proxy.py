from abc import abstractmethod

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
        proxy_update: ProxyInfoUpdateSchema,
        *,
        id: int,
    ) -> ProxyInfoSchema:
        """Updates proxy info if it exist.
        Updates info in db by `id`.
        Restarts proxy engine with new info.

        Raises:
            ValueError: If info not exist.
            RuntimeError: If xray restarted with error.
        Returns:
            Updated info if it updated success.
        """
