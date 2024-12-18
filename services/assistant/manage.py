import sys
import asyncio
from fastapi import FastAPI
import uvicorn

from app.infra.config import settings
from app.infra.logging import logger, config

from dependencies import AssistantDependencies

from app.app import AppFactory
from app.adapters.input.bot import BotAppFactory, BotServicesFactory, BotSettings


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

        factory = AppFactory(logger)
        factory.register_sub_factory(bot_factory)

        return factory.create_app()

    uvicorn.run(
        app=create_app(dependencies),
        host=settings.host,
        port=settings.port,
        log_config=config,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
    )


def run_worker(dependencies: AssistantDependencies):
    worker = dependencies.celery_connector.celery.Worker(concurrency=1)

    worker.start()


def run_sheduled_tasks(dependencies: AssistantDependencies):
    result = dependencies.restart_proxy.task.delay()
    print(result.id)
    # Example tasks entry point for future.
    # from app.schemas.availability import Service

    # async def start():
    #     async with dependencies.create_availability_service() as avail_service:
    #         await avail_service.check_availability(Service.xray)

    # asyncio.run(start())


def run():
    dependencies = AssistantDependencies(settings, logger)

    args = sys.argv

    if "-t" in args:
        run_sheduled_tasks(dependencies)
    elif "-w" in args:
        run_worker(dependencies)
    else:
        run_backend(dependencies)

    asyncio.run(dependencies.close_dependencies())


if __name__ == "__main__":
    run()
