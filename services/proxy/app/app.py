from contextlib import asynccontextmanager
from fastapi import FastAPI

from common.logging import logger
from common.config import generate
from common.messaging.bus import MessageBus

from app.container import Container
from app.infra.config import Settings
from app.controllers import admin


async def init_bus(container: Container) -> MessageBus:
    bus: MessageBus = await container.message_bus()
    scope_event = container.scope_event()
    uuid_event = container.uuid_event()
    auth_service = container.auth_service()

    uuid_event.register_dispatcher(bus.process_out)

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
    container.wire(
        modules=[
            "app.controllers.admin.main",
            "app.controllers.admin.views",
        ]
    )

    app = FastAPI(redoc_url=None, docs_url=None, lifespan=create_lifespan(container))
    app.container = container

    admin.register_admin(
        app,
        username=settings.admin_username,
        password=settings.admin_password,
    )

    return app


app = create_app()
