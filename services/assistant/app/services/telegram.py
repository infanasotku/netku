from app.contracts.services import BotService


class BotServiceImpl(BotService):
    async def send_notify_by_subscriptions(self, subscriptions: list[str]) -> None:
        raise NotImplementedError
