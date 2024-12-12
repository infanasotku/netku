from abc import ABC, abstractmethod


class TelegramClient(ABC):
    @abstractmethod
    async def send_message(message: str, id: int):
        """Sends message to user by his id."""
