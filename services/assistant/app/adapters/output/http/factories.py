from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiogram import Bot

from app.adapters.output.http.assistant import HTTPAssistantClient
from app.adapters.output.http.notification import AiogramNotificationClient


class HTTPAssistantClientFactory:
    def __init__(self, assistant_addr: str):
        self.assistant_addr = assistant_addr
        self.instance: HTTPAssistantClient = None

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[HTTPAssistantClient, None]:
        """:return: instance of `HTTPAssistantlient`."""
        if self.instance is None:
            self.instance = HTTPAssistantClient(self.assistant_addr)

        yield self.instance


class AiogramNotificationClientFactory:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.instance: AiogramNotificationClient = None

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[AiogramNotificationClient, None]:
        """:return: instance of `AiogramNotificationClient`."""
        if self.instance is None:
            self.instance = AiogramNotificationClient(self.bot)

        yield self.instance
