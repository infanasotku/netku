from app.contracts.clients import BotClient
from app.contracts.services import BotService, UserService


class BotServiceImpl(BotService):
    def __init__(self, bot_client: BotClient, user_service: UserService):
        self._bot_client = bot_client
        self._user_service = user_service

    async def send_notify_by_subscriptions(
        self, subscriptions: list[str], message: str
    ) -> None:
        users = await self._user_service.get_users_by_active_subscriptions(
            subscriptions, True
        )

        for user in users:
            if user.telegram_id is not None:
                await self._bot_client.send_message(message, user.telegram_id)
