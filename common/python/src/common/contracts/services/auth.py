from abc import abstractmethod
from collections.abc import Iterable
from common.contracts.client import BaseClient
from common.schemas.client_credential import ClientCredentials


class AuthService(BaseClient):
    @abstractmethod
    async def authorize(
        self, token: str, needed_scopes: Iterable[str]
    ) -> ClientCredentials | None:
        """Authorizes client by `token` and checks his access with `needed_scopes`.

        Returns:
            Client credential if client has access, `None` otherwise.
        """
