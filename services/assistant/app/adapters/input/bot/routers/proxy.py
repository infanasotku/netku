from logging import Logger
from aiogram import Dispatcher, Router
from aiogram.types import (
    Message,
)
from aiogram.filters import Command
from aiogram.utils.markdown import hbold

from app.contracts.protocols import CreateService
from app.contracts.services import (
    UserService,
    XrayService,
)

from app.schemas.user import Subscription

import app.adapters.input.bot.utils as utils
import app.adapters.input.bot.text as text

from app.adapters.input.bot.routers.base import BaseRouter


class ProxyRouter(BaseRouter):
    def __init__(
        self,
        create_user_service: CreateService[UserService],
        create_xray_service: CreateService[XrayService],
        logger: Logger,
    ):
        self.create_user_service = create_user_service
        self.create_xray_service = create_xray_service
        self.router = Router(name="main")
        self.logger = logger

    def register_router(self, dp: Dispatcher):
        self._register_handlers()
        dp.include_router(self.router)

    def _register_handlers(self):
        self.router.message.register(self._subscribe_for_proxy, Command("proxy"))
        self.router.message.register(self._get_proxy_uuid, Command("proxy_uid"))

    async def _subscribe_for_proxy(self, message: Message):
        async with self.create_user_service() as user_service:
            user = await user_service.get_user_by_telegram_id(message.chat.id)

            if not user:
                return await message.answer(text.please_click_start)

            if user.proxy_subscription:
                return await message.answer("You already subscribeted to proxy!")

            await utils.subscribe_user(
                user, Subscription.proxy_subscription, user_service
            )

        await message.answer("You subscribeted to proxy!")

    async def _get_proxy_uuid(self, message: Message):
        async with self.create_user_service() as user_service:
            user = await user_service.get_user_by_telegram_id(message.chat.id)

        if not user:
            return await message.answer(text.please_click_start)

        if not user.proxy_subscription:
            return await message.answer("You didn't subscribe to proxy!")

        async with self.create_xray_service() as xray_service:
            uid = await xray_service.get_current_uid()

        if not uid:
            return await message.answer(hbold("Proxy inactive"))

        return await message.answer(hbold(uid))
