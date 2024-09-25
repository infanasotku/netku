from fastapi_utils.tasks import repeat_every

from db import service
from settings import logger, settings
from xray import xray

from bot.bot import bot
import bot.text as text


@repeat_every(seconds=settings.xray_restart_minutes * 60, logger=logger)
async def restart_proxy():
    """Restarts proxy and sends `id` to all user subscripted to proxy."""
    logger.info("Proxy subscription performing.")

    uid = await xray.restart()

    if not uid:
        logger.info("Proxy subscription performed.")
        return

    users = service.get_users()

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
