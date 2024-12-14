from app.contracts.services import TelegramService


class TelegramServiceImpl(TelegramService):
    async def send_notify_by_subscriptions(self, subscriptions: list[str]) -> None:
        raise NotImplementedError
