from logging import Logger
from aiogram import Bot
from celery import Celery

from app.contracts.services import UserService, XrayService
from app.contracts.protocols import CreateService

import app.adapters.input.bot.text as text
from app.adapters.tasks.task import CeleryTask


class RestartProxyTask(CeleryTask):
    def __init__(
        self,
        logger: Logger,
        celery: Celery,
        bot: Bot,
        create_user_service: CreateService[UserService],
        create_xray_service: CreateService[XrayService],
    ):
        super().__init__("restart_proxy", logger, celery)
        self.bot = bot
        self.create_user_service = create_user_service
        self.create_xray_service = create_xray_service

    async def _run(self):
        """Restarts proxy and sends `id` to all user subscripted to proxy."""
        self._logger.info("Proxy subscription performing.")

        async with self.create_xray_service() as xray:
            uid = await xray.restart_xray()

        if not uid:
            self._logger.warning("Proxy subscription failed - xray didn't restarted.")
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
                self._logger.warning(f"Error occured while sending proxy uid: {e}.")

        self._logger.info("Proxy subscription performed.")
