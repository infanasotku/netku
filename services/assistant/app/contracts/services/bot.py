from abc import abstractmethod

from app.contracts.services.base import BaseService


class BotService(BaseService):
    @abstractmethod
    async def send_notify_by_subscriptions(
        self, subscriptions: list[str], message: str
    ) -> None:
        """Sends `message` to all users with active `subscriptions`."""
