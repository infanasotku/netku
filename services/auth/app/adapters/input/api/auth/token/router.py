from fastapi import APIRouter, Body, HTTPException, status
from fastapi.security import HTTPBearer

from common.contracts.protocols import CreateService
from app.contracts.services import ClientService

from app.schemas.token import TokenPayload, TokenSchema


class TokenRouter:
    def __init__(self, create_client_service: CreateService[ClientService]):
        self._create_client_service = create_client_service

        self.router = APIRouter()
        self.security = HTTPBearer()

        self.router.add_api_route("/", self.create_token, methods=["POST"])
        self.router.add_api_route(
            "/introspect", self.introspect_token, methods=["POST"]
        )

    async def create_token(
        self, client_id: str = Body(), client_secret: str = Body()
    ) -> TokenSchema:
        """Creates token for specified `client_id` and `client_secret`.

        Returns:
            Token with type if client authenticated.

        Raises:
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED):
                If error occured with client credentials.
        """
        async with self._create_client_service() as service:
            token = await service.authenticate(client_id, client_secret)
            if token is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return token

    async def introspect_token(self, token: str) -> TokenPayload:
        """Introspects `token`.

        Returns:
            Token payload with token introspection
            if client authenticated.
        """
        async with self._create_client_service() as service:
            return await service.authorize(token)
