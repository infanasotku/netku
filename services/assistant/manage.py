import sys
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
    dependencies.register_task_worker()
    dependencies.worker.start()


def run_sheduled_tasks(dependencies: AssistantDependencies):
    dependencies.register_sheduled_tasks()
    dependencies.beat.run()


def run():
    dependencies = AssistantDependencies(settings, logger)

    args = sys.argv

    if "-t" in args:
        run_sheduled_tasks(dependencies)
    elif "-w" in args:
        run_worker(dependencies)
    else:
        run_backend(dependencies)

    dependencies.close_dependencies()


if __name__ == "__main__":
    run()
