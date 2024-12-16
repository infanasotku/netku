from aiogram import Bot

from app.contracts.clients import NotificationClient
from app.schemas.user import UserSchema
from app.adapters.output.http.base import HTTPClient


class AiogramNotificationClient(HTTPClient, NotificationClient):
    def __init__(self, bot: Bot):
        self._bot = bot

    async def send_message(self, message: str, user: UserSchema):
        await self._bot.send_message(user.telegram_id, message)
