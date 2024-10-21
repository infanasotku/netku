from logging import Logger
from typing import AsyncContextManager, Callable
from fastapi_utils.tasks import repeat_every
from aiogram import Bot

from services import UserService, XrayService

import bot.text as text


def restart_proxy_factory(
    xray_restart_minutes: float,
    logger: Logger,
    bot: Bot,
    create_user_service: Callable[[], AsyncContextManager[UserService]],
    create_xray_service: Callable[[], AsyncContextManager[XrayService]],
):
    """Creates restart proxy task."""

    @repeat_every(seconds=xray_restart_minutes * 60, logger=logger)
    async def restart_proxy():
        """Restarts proxy and sends `id` to all user subscripted to proxy."""
        logger.info("Proxy subscription performing.")

        async with create_xray_service() as xray:
            uid = await xray.restart_xray()

        if not uid:
            logger.warning("Proxy subscription failed - xray didn't restarted.")
            return

        async with create_user_service() as service:
            users = await service.get_users()

        for user in users:
            if not user.telegram_id or not user.proxy_subscription:
                continue

            try:
                await bot.send_message(
                    user.telegram_id, text.generate_proxy_task_message(uid)
                )
            except Exception as e:
                logger.warning(f"Error occured while sending proxy uid: {e}.")

        logger.info("Proxy subscription performed.")

    return restart_proxy
