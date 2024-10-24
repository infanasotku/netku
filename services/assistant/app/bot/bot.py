import asyncio
from logging import Logger
from typing import Annotated, Any, AsyncContextManager, AsyncGenerator, Callable
from fastapi import FastAPI, Header
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update, WebhookInfo, BotCommand
import aiogram.loggers as aloggers
from pydantic import BaseModel

from app.app import AbstractAppFactory
from app.services import (
    AbstractBookingService,
    AbstractUserService,
    AbstractXrayService,
)
from app.bot.router import MainRouter
from app.bot import tasks


class BotServicesFactory(BaseModel):
    create_user_service: Callable[[], AsyncContextManager[AbstractUserService]]
    create_booking_service: Callable[[], AsyncContextManager[AbstractBookingService]]
    create_xray_service: Callable[[], AsyncContextManager[AbstractXrayService]]


class BotSettings(BaseModel):
    bot_token: str
    telegram_token: str
    bot_webhook_url: str
    xray_restart_minutes: float


class BotFactory(AbstractAppFactory):
    def __init__(
        self,
        bot_settings: BotSettings,
        bot_services_factory: BotServicesFactory,
        logger: Logger,
    ):
        self.route_path = "/bot"
        self.settings = bot_settings
        self.logger = logger
        self.bot_service_factory = bot_services_factory

        self.dispatcher = Dispatcher()
        self.bot = Bot(
            token=self.settings.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        # Disables aiogram loggers
        aloggers.dispatcher.propagate = False
        aloggers.event.propagate = False
        aloggers.middlewares.propagate = False
        aloggers.scene.propagate = False
        aloggers.webhook.propagate = False

    def create_app(self) -> FastAPI:
        app = FastAPI(docs_url=None, redoc_url=None)
        app.add_api_route(path="/webhook", endpoint=self._webhook, methods=["POST"])
        main_router = MainRouter(
            create_booking_service=self.bot_service_factory.create_booking_service,
            create_user_service=self.bot_service_factory.create_user_service,
            create_xray_service=self.bot_service_factory.create_xray_service,
            logger=self.logger,
        )
        main_router.register_router(self.dispatcher)

        return app

    def create_lifespan(self) -> Callable[[FastAPI], AsyncGenerator[Any, None]]:
        async def _lifespan(_: FastAPI) -> AsyncGenerator:
            self.logger.info("Registrating bot webhook")
            await self.bot.delete_webhook(drop_pending_updates=True)

            await self.bot.set_webhook(
                url=self.settings.bot_webhook_url,
                secret_token=self.settings.telegram_token,
                allowed_updates=self.dispatcher.resolve_used_update_types(),
                drop_pending_updates=True,
            )
            await self.bot.set_my_commands(
                [
                    BotCommand(command="start", description="Registration"),
                    BotCommand(command="stop", description="Cancels all subscriptions"),
                    BotCommand(command="proxy", description="Subscribe to proxy"),
                    BotCommand(command="proxy_uid", description="Get proxy uid"),
                    BotCommand(
                        command="machine_booking", description="Machinge booking menu"
                    ),
                ]
            )
            self.logger.info(
                "Webhook info: " + str(await self._webhook_info()).split()[0]
            )

            self.logger.info("Starting bot tasks")
            restart_proxy = tasks.restart_proxy_factory(
                self.settings.xray_restart_minutes,
                self.logger,
                self.bot,
                self.bot_service_factory.create_user_service,
                self.bot_service_factory.create_xray_service,
            )
            task_list: list[asyncio.Task] = [asyncio.create_task(restart_proxy())]
            self.logger.info("Bot tasks started")
            yield
            for task in task_list:
                task.cancel()

        return _lifespan

    async def _webhook(
        self,
        update: dict,
        x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
    ):
        """Registers webhook endpoint for telegram bot"""
        if x_telegram_bot_api_secret_token != self.settings.telegram_token:
            self.logger.error("Wrong secret token!")
            return {"status": "error", "message": "Wrong secret token !"}
        try:
            answer = await self.dispatcher.feed_update(
                bot=self.bot, update=Update(**update)
            )
            return answer
        except Exception as e:
            self.logger.error(f"Unhandled error occured: {e}")
            return

    async def _webhook_info(self) -> WebhookInfo | None:
        return await self.bot.get_webhook_info()
