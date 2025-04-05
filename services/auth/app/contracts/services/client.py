from abc import abstractmethod

from common.contracts.services import AuthService

from app.schemas.client import ClientFullSchema
from app.schemas.token import TokenSchema


class ClientService(AuthService):
    @abstractmethod
    async def get_client_with_scopes_by_external_client_id(
        self,
        external_client_id: int,
    ) -> ClientFullSchema | None:
        """Gets client with scopes by `ClientSchema.external_client_id`.

        Returns:
            Client if it exist in db, `None` otherwise.
        """

    @abstractmethod
    async def authenticate(
        self, external_client_id: int, client_secret: str
    ) -> TokenSchema | None:
        """Authenticates client

        Returns:
            Token with client scopes if client authenticated,
            `None` otherwise.
        """

    @abstractmethod
    async def remove_client_scope(self, client_scope_id: int) -> list[str]:
        """Removes client scope.

        Sends corresponding change event.

        Returns:
            Relevant client scopes.
        """

    @abstractmethod
    async def create_client_scope(
        self, external_client_id: int, scope_id: int
    ) -> list[str]:
        """Creates client scope.

        Sends corresponding change event.

        Returns:
             Relevant client scopes.
        """
