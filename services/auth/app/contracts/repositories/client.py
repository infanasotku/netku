from abc import abstractmethod

from common.contracts.repository import BaseRepository

from app.schemas.client import ClientSchema


class ClientRepository(BaseRepository):
    @abstractmethod
    async def get_client_by_client_id(self, client_id: int) -> ClientSchema | None:
        pass
