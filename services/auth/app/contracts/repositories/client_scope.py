from abc import abstractmethod

from common.contracts.repository import BaseRepository


class ClientScopeRepository(BaseRepository):
    @abstractmethod
    async def get_client_id_by_client_scope_id(self, client_scope_id: int) -> int:
        pass

    @abstractmethod
    async def get_scopes_by_client_id(self, client_id: int) -> list[str]:
        pass

    @abstractmethod
    async def remove_client_scope(self, client_scope_id: int):
        pass
        """Removes client scope.

        Returns:
            Relevant client scopes.
        """
        pass
