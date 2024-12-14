from abc import abstractmethod
from aiogram import Router

from app.contracts.services.base import BaseService


class BotService(BaseService):
    @abstractmethod
    async def register_router(self, router: Router) -> None:
        """Registers router for telegram bot."""

    @abstractmethod
    async def feed_update(
        self,
        update: dict,
    ) -> None:
        """Equivalent of Dispatcher.feed_update"""

    @abstractmethod
    async def send_notify_by_subscriptions(self, subscriptions: list[str]) -> None:
        """Sends notify to all users with active `subscriptions`."""
