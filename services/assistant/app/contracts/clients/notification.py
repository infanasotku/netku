from abc import abstractmethod

from app.schemas.user import UserSchema
from app.contracts.clients.base import BaseClient


class NotificationClient(BaseClient):
    """Client for sending notifies to users."""

    @abstractmethod
    async def send_message(self, message: str, user: UserSchema):
        """Sends message to user."""

    @abstractmethod
    async def send_subscription_message(
        self, message: str, subscription: str, user: UserSchema
    ):
        """Sends subscription message to user."""

    @abstractmethod
    def highlight(self, message: str, sep: str = "/") -> str:
        """Highlights message between `sep`.

        :return: highlighted message."""
