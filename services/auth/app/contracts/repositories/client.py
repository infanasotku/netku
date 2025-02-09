from abc import abstractmethod

from common.contracts.repository import BaseRepository

from app.schemas.client import ClientSchema


class ClientRepository(BaseRepository):
    @abstractmethod
    async def get_client_by_external_client_id(
        self, external_client_id: int
    ) -> ClientSchema | None:
        pass
