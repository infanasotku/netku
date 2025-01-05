from abc import abstractmethod

from common.contracts.service import BaseService

from app.schemas.client import ClientSchema


class ClientService(BaseService):
    @abstractmethod
    async def authenticate(client_id: str, client_secret: str) -> ClientSchema | None:
        """Authenticates client
        :return: Client if it authenticated, `None` otherwise."""

    @abstractmethod
    async def authorize(token: str, needed_scopes: list[str]) -> ClientSchema | None:
        """Authenticates client
        :return: Client if it authenticated, `None` otherwise."""
