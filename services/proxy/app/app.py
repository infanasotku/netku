from contextlib import asynccontextmanager
from fastapi import FastAPI

from common.logging import logger
from common.config import generate
from common.messaging.bus import MessageBus

from app.container import Container
from app.infra.config import Settings


async def init_bus(container: Container) -> MessageBus:
    bus: MessageBus = await container.message_bus()
    scope_event = container.scope_event()
    auth_service = container.auth_service()

    scope_event.register_handler(auth_service.process_update)
    bus.register_event(scope_event)

    return bus


def create_lifespan(container: Container):
    @asynccontextmanager
    async def lifespan(_):
        try:
            await container.init_resources()
            bus = await init_bus(container)
            await bus.run()
            yield
        finally:
            await bus.stop()
            await container.shutdown_resources()

    return lifespan


def create_app() -> FastAPI:
    settings = generate(Settings, logger)
    container = Container(logger=logger)
    container.config.from_pydantic(settings)

    app = FastAPI(redoc_url=None, docs_url=None, lifespan=create_lifespan(container))
    app.container = container

    return app


app = create_app()
