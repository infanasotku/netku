from abc import abstractmethod

from common.contracts.services import AuthService, BaseService

from app.schemas.client import ClientFullSchema
from app.schemas.token import TokenPayload, TokenSchema


class ClientService(BaseService, AuthService):
    @abstractmethod
    async def get_client_with_scopes_by_client_id(
        self,
        client_id: int,
    ) -> ClientFullSchema | None:
        """Gets client with scopes by `ClientSchema.client_id`.

        Returns:
            Client if it exist in db, `None` otherwise.
        """

    @abstractmethod
    async def authenticate(
        self, client_id: str, client_secret: str
    ) -> TokenSchema | None:
        """Authenticates client

        Returns:
            Token with client scopes if client authenticated,
            `None` otherwise.
        """

    @abstractmethod
    async def introspect(self, token: str) -> TokenPayload | None:
        """Introspects `token`.

        Returns:
            Token payload with token introspection
            if client authenticated, `None` otherwise.
        """
