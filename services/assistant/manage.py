import asyncio
from fastapi import FastAPI
import uvicorn

from app.infra.config import settings
from app.infra.logging import logger, config

from dependencies import AssistantDependencies

from app.app import AppFactory
from app.adapters.bot import BotAppFactory, BotServicesFactory, BotSettings
from app.tasks.restart_proxy import RestartProxyTask


def run_backend(dependencies: AssistantDependencies):
    def create_app(dependencies: AssistantDependencies) -> FastAPI:
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

    uvicorn.run(
        app=create_app(dependencies),
        host=settings.host,
        port=settings.port,
        log_config=config,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
    )


def run_sheduled_tasks(dependencies: AssistantDependencies):
    from app.schemas.availability import Service

    async def start():
        async with dependencies.create_availability_service() as avail_service:
            await avail_service.check_availability(Service.xray)

    asyncio.run(start())


def run():
    param = "shedule"

    dependencies = AssistantDependencies(settings)

    if param == "shedule":
        run_sheduled_tasks(dependencies)
    else:
        run_backend(dependencies)


if __name__ == "__main__":
    run()
