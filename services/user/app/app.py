from contextlib import asynccontextmanager
from fastapi import FastAPI

from common.messaging.bus import MessageBus
from common.logging import logger
from common.config import generate
from common.events.scope import ScopeChangedEvent
from common.schemas.client_credential import ClientCredentials

from app.container import Container
from app.infra.config import Settings
from app.controllers import api
from app.controllers import admin


# {"event": "scope_changed", "payload":в {"external_client_id": "test", "scopes": ["kek", "lol"]}}
async def init_bus(container: Container) -> MessageBus:
    bus: MessageBus = await container.message_bus()

    def test(creds: ClientCredentials):
        print("--------------------")
        print(creds)
        print("--------------------")

    scope_event = ScopeChangedEvent()
    scope_event.register_handler(test)
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
            "app.controllers.api.router",
        ]
    )

    app = FastAPI(redoc_url=None, docs_url=None, lifespan=create_lifespan(container))
    app.container = container

    admin.register_admin(
        app,
        username=settings.admin_username,
        password=settings.admin_password,
    )
    app.mount("/api", api.create_api())

    return app


app = create_app()
