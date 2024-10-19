import logging
import pathlib
import sys
from fastapi import FastAPI
import uvicorn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

sys.path.append((pathlib.Path(__file__).parent.parent).resolve().as_posix())
from settings import settings, logger
from app import AppFactory
from bot import BotFactory, BotServiceFactories, BotSettings
from database import get_db_factory
from services import UserServiceFactory, BookingServiceFactory


def create_app() -> FastAPI:
    async_engine = create_async_engine(settings.psql_dsn)
    async_session = async_sessionmaker(async_engine)
    get_db = get_db_factory(async_session)
    us_factory = UserServiceFactory(get_db)
    bs_factory = BookingServiceFactory(get_db)

    # bot
    bot_factory = BotFactory(
        bot_settings=BotSettings(**settings.model_dump()),
        bot_service_factories=BotServiceFactories(
            user_service_factory=us_factory.create_user_service,
            booking_service_factory=bs_factory.create_booking_service,
        ),
        logger=logger,
    )

    factory = AppFactory(bot_factory)
    return factory.create_app()


def run():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:     [%(asctime)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )
    log_config_path = settings.app_directory_path + "/log_config.yaml"

    uvicorn.run(
        app=create_app(),
        host=settings.host,
        port=settings.port,
        log_config=log_config_path,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
    )


if __name__ == "__main__":
    run()
