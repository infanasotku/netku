from abc import abstractmethod

from common.contracts.services import BaseService

from app.schemas.proxy import (
    ProxyInfoCreateSchema,
    ProxyInfoSchema,
    ProxyInfoUpdateSchema,
)


class ProxyService(BaseService):
    @abstractmethod
    async def get_proxy_info(self) -> ProxyInfoSchema | None:
        """
        Returns:
            Proxy info if it exist in db, `None` otherwise.
        """

    @abstractmethod
    async def create_proxy_info(
        self, proxy_create: ProxyInfoCreateSchema
    ) -> ProxyInfoSchema:
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

    @abstractmethod
    async def sync_with_proxy(self) -> ProxyInfoSchema:
        """Syncs saved proxy info with xray by restarting it.

        Sends corresponding event about info changing.

        Raises:
            ValueError: If info already synced or not exist.
            RuntimeError: If xray restarted with error.
        Returns:
            Synced proxy info.
        """

    @abstractmethod
    async def pull_from_proxy(self) -> ProxyInfoSchema:
        """Pulls full proxy info and saves it in db.

        Returns:
            Pulled info.
        """
