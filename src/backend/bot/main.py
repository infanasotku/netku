from typing import Annotated, AsyncGenerator, Callable
from fastapi import FastAPI, Header
from aiogram.types import Update, WebhookInfo, BotCommand
import aiogram.loggers as aloggers

from settings import settings
from bot.bot import bot, dispatcher, logger
from bot.router import router


def create() -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None)
    _configure(app)
    return app


def create_lifespan() -> Callable[[FastAPI], AsyncGenerator]:
    async def _lifespan(_: FastAPI) -> AsyncGenerator:
        await bot.delete_webhook(drop_pending_updates=True)

        await bot.set_webhook(
            url=settings.bot_webhook_url,
            secret_token=settings.telegram_token,
            allowed_updates=dispatcher.resolve_used_update_types(),
            drop_pending_updates=True,
        )
        await bot.set_my_commands(
            [BotCommand(command="start", description="Регистрирует подписку")]
        )
        logger.info("Webhook info: " + str(await _webhook_info()).split()[0])
        yield

    return _lifespan


def _configure(bot: FastAPI):
    bot.add_api_route(path="/webhook", endpoint=_webhook, methods=["POST"])
    dispatcher.include_router(router)

    # Disables aiogram loggers
    aloggers.dispatcher.propagate = False
    aloggers.event.propagate = False
    aloggers.middlewares.propagate = False
    aloggers.scene.propagate = False
    aloggers.webhook.propagate = False


async def _webhook(
    update: dict,
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
):
    """Registers webhook endpoint for telegram bot"""
    if x_telegram_bot_api_secret_token != settings.telegram_token:
        logger().error("Wrong secret token !")
        return {"status": "error", "message": "Wrong secret token !"}
    try:
        answer = await dispatcher.feed_update(bot=bot, update=Update(**update))
        return answer
    except Exception as e:
        logger.error(f"Bot unhandled error: {e}")
        return


async def _webhook_info() -> WebhookInfo | None:
    return await bot.get_webhook_info()
