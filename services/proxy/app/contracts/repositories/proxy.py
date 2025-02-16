from abc import abstractmethod
from typing import NoReturn

from common.contracts.repository import BaseRepository

from app.schemas.proxy import (
    ProxyInfoSchema,
    ProxyInfoCreateSchema,
    ProxyInfoUpdateSchema,
)


class ProxyInfoRepository(BaseRepository):
    @abstractmethod
    async def get_proxy_info(self) -> ProxyInfoSchema | None:
        """
        Returns:
            Proxy info if it exist in db, `None` otherwise.
        """

    @abstractmethod
    async def create_proxy_info(
        self, proxy_create: ProxyInfoCreateSchema
    ) -> ProxyInfoSchema | NoReturn:
        """Creates proxy info if it not exist in db.
        Raises:
            ValueError: If info already exist.
        Returns:
            Created info if it created success.
        """

    @abstractmethod
    async def update_proxy_info(
        self, proxy_update: ProxyInfoUpdateSchema
    ) -> ProxyInfoSchema:
        """Updates proxy info if it exist in db.
        Raises:
            ValueError: If info not exist.
        Returns:
            Updated info if it updated success.
        """
