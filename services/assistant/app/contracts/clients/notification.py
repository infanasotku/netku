from abc import abstractmethod

from app.schemas.user import UserSchema
from app.contracts.clients.base import BaseClient


class NotificationClient(BaseClient):
    """Client for sending notifies to users."""

    @abstractmethod
    async def send_message(self, message: str, user: UserSchema):
        """Sends message to user."""
