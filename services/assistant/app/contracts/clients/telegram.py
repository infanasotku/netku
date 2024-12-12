from abc import abstractmethod

from app.contracts.clients.base import BaseClient


class TelegramClient(BaseClient):
    @abstractmethod
    async def send_message(self, message: str, id: int):
        """Sends message to user by his id."""
