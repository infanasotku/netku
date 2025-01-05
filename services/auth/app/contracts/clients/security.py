from abc import abstractmethod

from common.contracts.client import BaseClient

from app.schemas.client import TokenPayload


class SecurityClient(BaseClient):
    @abstractmethod
    def get_hash(self, source: str) -> str:
        """:return: Hashed `source`."""

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Checks if the password matches the hashed password"""
        return self.get_hash(plain_password) == hashed_password

    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        """Creates access token with `data`."""

    @abstractmethod
    def parse_access_token(self, token: str) -> TokenPayload:
        pass
