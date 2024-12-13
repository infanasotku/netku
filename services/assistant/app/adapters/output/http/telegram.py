from aiogram import Bot
from app.contracts.clients.telegram import TelegramClient

from app.adapters.output.http.base import HTTPClient


class HTTPTelegramClient(HTTPClient, TelegramClient):
    def __init__(self, bot: Bot):
        self._bot = bot

    async def send_message(self, message: str, id: int):
        await self._bot.send_message(id, message)