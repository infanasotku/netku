from aiogram import Bot
from aiogram.utils.markdown import hbold

from app.contracts.clients import NotificationClient
from app.schemas.user import UserSchema
from app.adapters.output.http.base import HTTPClient


class AiogramNotificationClient(HTTPClient, NotificationClient):
    def __init__(self, bot: Bot):
        self._bot = bot

    def _generate_subscription_message(self, message: str, subscription: str) -> str:
        """Generates template message text for `subscription` with `message`."""
        header = hbold(f"[{subscription} subscription]:")
        body = message

        return "\n".join([header, body])

    def highlight(self, message: str, sep: str = "/") -> str:
        msgs = message.split(sep)

        for i in range(1, len(msgs), 2):
            msgs[i] = hbold(msgs[i])

        return "".join(msgs)

    async def send_message(self, message: str, user: UserSchema):
        await self._bot.send_message(user.telegram_id, message)

    async def send_subscription_message(
        self, message: str, subscription: str, user: UserSchema
    ):
        msg = self._generate_subscription_message(message, subscription)

        await self.send_message(msg, user)
