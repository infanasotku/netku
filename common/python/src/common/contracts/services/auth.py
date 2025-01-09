from abc import abstractmethod

from common.contracts.client import BaseClient
from common.schemas.token import TokenPayload


class AuthService(BaseClient):
    @abstractmethod
    async def introspect(self, token: str) -> TokenPayload | None:
        """Introspects `token`.

        Returns:
            Token payload with token introspection
            if client authenticated, `None` otherwise.
        """
