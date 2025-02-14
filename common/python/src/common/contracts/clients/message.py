from abc import abstractmethod
from typing import Protocol, Any

from common.contracts.clients.base import BaseClient


class MessageHandler(Protocol):
    def __call__(self, message: str, *, headers: dict[str, Any]): ...


class MessageOutClient(BaseClient):
    @abstractmethod
    async def send(self, message: str):
        """Sends `message` to broker."""


class MessageInClient(BaseClient):
    @abstractmethod
    def register(self, handler: MessageHandler):
        """Registers callback for handling messages."""

    @abstractmethod
    async def run(self):
        """Runs receiving messages."""
