from aiogram import Router

from app.contracts.services import TelegramService


class BookingServiceImpl(TelegramService):
    async def register_router(self, router: Router) -> None:
        raise NotImplementedError

    async def feed_update(
        self,
        update: dict,
    ) -> None:
        raise NotImplementedError

    async def send_notify_by_subscriptions(self, subscriptions: list[str]) -> None:
        raise NotImplementedError
