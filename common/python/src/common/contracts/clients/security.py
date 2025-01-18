from abc import abstractmethod

from common.contracts.clients.base import BaseClient
from common.schemas.token import TokenPayload


class SecurityClient(BaseClient):
    @abstractmethod
    def get_hash(self, source: str) -> str:
        """
        Returns:
            Hashed `source`.
        """

    def verify_source(self, plain_source: str, hashed_source: str) -> bool:
        """Checks if the source matches the hashed source"""
        return self.get_hash(plain_source) == hashed_source

    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        """Creates access token with `data`."""

    @abstractmethod
    def parse_access_token(self, token: str) -> TokenPayload | None:
        """Parses access token.

        Returns:
            Token payload if it parse success, `None` otherwise.
        """
