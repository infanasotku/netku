import asyncio
from abc import abstractmethod
from typing import Protocol, Any

from common.contracts.clients.base import BaseClient


class MessageHandler(Protocol):
    def __call__(self, message: str, *, headers: dict[str, Any]): ...


class MessageOutClient(BaseClient):
    @abstractmethod
    async def send(self, message: str, *, headers: dict[str, Any]):
        """Sends `message` to broker."""


def _is_async_callable(obj) -> bool:
    return asyncio.iscoroutinefunction(obj) or (
        callable(obj) and asyncio.iscoroutinefunction(obj.__call__)
    )


class MessageInClient(BaseClient):
    def __init__(self):
        self._handler = None

    def register(self, handler: MessageHandler):
        """Registers callback for handling messages."""
        if not _is_async_callable(handler):
            raise TypeError("Handler must be async.")
        self._handler = handler

    @abstractmethod
    async def run(self):
        """Runs receiving messages."""
