from fastapi import FastAPI
import uvicorn

from app.infra.config import settings
from app.infra.logging import logger, config

from dependencies import AssistantDependencies

from app.app import AppFactory
from app.adapters.bot import BotAppFactory, BotServicesFactory, BotSettings
from app.tasks.restart_proxy import RestartProxyTask


def create_app() -> FastAPI:
    dependencies = AssistantDependencies(settings)

    bot_factory = BotAppFactory(
        bot=dependencies.bot,
        bot_settings=BotSettings(**settings.model_dump()),
        bot_services_factory=BotServicesFactory(
            create_user_service=dependencies.create_user_service,
            create_booking_service=dependencies.create_booking_service,
            create_xray_service=dependencies.create_xray_service,
            create_booking_analysis_service=dependencies.create_booking_analysis_service,
        ),
        logger=logger,
    )

    # Tasks
    restart_proxy = RestartProxyTask(
        bot=dependencies.bot,
        create_user_service=dependencies.create_user_service,
        create_xray_service=dependencies.create_xray_service,
        logger=logger,
        xray_restart_minutes=settings.xray_restart_minutes,
    )

    factory = AppFactory(logger)
    factory.register_sub_factory(bot_factory)

    factory.register_task(restart_proxy)

    return factory.create_app()


def run():
    uvicorn.run(
        app=create_app(),
        host=settings.host,
        port=settings.port,
        log_config=config,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
    )


if __name__ == "__main__":
    run()
