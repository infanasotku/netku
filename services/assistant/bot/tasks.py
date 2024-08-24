from db import service

from bot.bot import bot
import bot.text as text
from settings import logger


async def send_proxy_id(id: str):
    """Sends new proxy `id` to all user subscripted to proxy."""
    logger.info("Proxy subscription performing.")

    users = service.get_users()

    for user in users:
        if not user.telegram_id or not user.proxy_subscription:
            continue

        try:
            await bot.send_message(
                user.telegram_id, text.generate_proxy_task_message(id)
            )
        except Exception as e:
            logger.warning(f"Error occured while sending proxy id: {e}.")

    logger.info("Proxy subscription performed.")
