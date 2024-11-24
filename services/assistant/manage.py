from fastapi import FastAPI
import uvicorn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.infra.config.settings import settings
from app.infra.logging.logger import logger, config
from app.app import AppFactory
from app.adapters.bot import BotFactory, BotServicesFactory, BotSettings
from app.infra.database.sql_db import get_db_factory
from app.infra.database.sql_db.repositories import (
    SQLBookingRepository,
    SQLUserRepository,
    SQLXrayRepository,
    SQLRepositoryFactory,
)
from app.services import UserServiceFactory, BookingServiceFactory, XrayServiceFactory
from app.adapters.output.grpc import BookingClientFactory, XrayClientFactory
from app.tasks.restart_proxy import RestartProxyTask


def create_app() -> FastAPI:
    # grpc client factories
    bc_factory = BookingClientFactory(
        client_addr=settings.booking_host,
        client_port=settings.booking_port,
        service_name="booking",
        reconnection_delay=settings.reconnection_delay,
        reconnection_retries=settings.reconnection_retries,
    )
    xc_factory = XrayClientFactory(
        client_addr=settings.xray_host,
        client_port=settings.xray_port,
        service_name="xray",
        reconnection_delay=settings.reconnection_delay,
        reconnection_retries=settings.reconnection_retries,
    )

    # db factory
    async_engine = create_async_engine(settings.psql_dsn)
    async_session = async_sessionmaker(async_engine)
    get_db = get_db_factory(async_session)
    br_factory = SQLRepositoryFactory(get_db, SQLBookingRepository)
    xr_factory = SQLRepositoryFactory(get_db, SQLXrayRepository)
    ur_factory = SQLRepositoryFactory(get_db, SQLUserRepository)

    # service factories
    us_factory = UserServiceFactory(ur_factory.create)
    bs_factory = BookingServiceFactory(br_factory.create, bc_factory.create)
    xs_factory = XrayServiceFactory(xr_factory.create, xc_factory.create)

    # Sub factories
    bot_factory = BotFactory(
        bot_settings=BotSettings(**settings.model_dump()),
        bot_services_factory=BotServicesFactory(
            create_user_service=us_factory.create,
            create_booking_service=bs_factory.create,
            create_xray_service=xs_factory.create,
        ),
        logger=logger,
    )

    # Tasks
    restart_proxy = RestartProxyTask(
        bot=bot_factory.bot,
        create_user_service=us_factory.create,
        create_xray_service=xs_factory.create,
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
