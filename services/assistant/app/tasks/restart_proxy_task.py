from logging import Logger
from typing import AsyncContextManager, Callable
from aiogram import Bot

from app.contracts.services import UserService, XrayService

import app.interfaces.bot.text as text

from app.tasks.task import Task


class RestartProxyTask(Task):
    def __init__(
        self,
        xray_restart_minutes: float,
        logger: Logger,
        bot: Bot,
        create_user_service: Callable[[], AsyncContextManager[UserService]],
        create_xray_service: Callable[[], AsyncContextManager[XrayService]],
    ):
        super().__init__("restart_proxy", xray_restart_minutes * 60, logger)
        self.bot = bot
        self.create_user_service = create_user_service
        self.create_xray_service = create_xray_service

    async def _run(self):
        """Restarts proxy and sends `id` to all user subscripted to proxy."""
        self.logger.info("Proxy subscription performing.")

        async with self.create_xray_service() as xray:
            uid = await xray.restart_xray()

        if not uid:
            self.logger.warning("Proxy subscription failed - xray didn't restarted.")
            return

        async with self.create_user_service() as service:
            users = await service.get_users()

        for user in users:
            if not user.telegram_id or not user.proxy_subscription:
                continue

            try:
                await self.bot.send_message(
                    user.telegram_id, text.generate_proxy_task_message(uid)
                )
            except Exception as e:
                self.logger.warning(f"Error occured while sending proxy uid: {e}.")

        self.logger.info("Proxy subscription performed.")
