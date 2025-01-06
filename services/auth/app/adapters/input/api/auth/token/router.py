from fastapi import APIRouter

from common.contracts.protocols import CreateService
from app.contracts.services import ClientService

from app.schemas.client import ClientOutSchema


class TokenRouter:
    def __init__(self, create_client_service: CreateService[ClientService]):
        self._create_client_service = create_client_service

        self.router = APIRouter()

    async def introspect_token(
        self, token: str, scopes: list[str]
    ) -> ClientOutSchema | None:
        """Introspects `token` for `scopes`.

        Returns:
            Client if token passed introspecting, `None` otherwise.
        """
        async with self._create_client_service() as service:
            return await service.authorize(token, scopes)
