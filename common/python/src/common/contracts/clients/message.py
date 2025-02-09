from abc import abstractmethod
from typing import Callable

from common.contracts.clients.base import BaseClient


class MessageOutClient(BaseClient):
    @abstractmethod
    async def send(self, message: str):
        """Sends `message` to broker."""


class MessageInClient(BaseClient):
    @abstractmethod
    def register(self, func: Callable[[str], None]):
        """Registers callback for handling messages."""

    @abstractmethod
    async def run(self):
        """Runs receiving messages."""
