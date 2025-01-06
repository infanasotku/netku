from abc import abstractmethod

from common.contracts.repository import BaseRepository


class ClientScopeRepository(BaseRepository):
    @abstractmethod
    async def get_scopes_by_client_id(self, id: int) -> list[str]:
        pass
