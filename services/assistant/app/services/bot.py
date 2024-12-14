from app.contracts.clients import BotClient
from app.contracts.services import BotService


class BotServiceImpl(BotService):
    def __init__(self, bot_client: BotClient):
        self._bot_client = bot_client

    async def send_notify_by_subscriptions(self, subscriptions: list[str]) -> None:
        raise NotImplementedError
