import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from common.contracts.clients import MessageInClient
from common.logging import logger, with_logging
from common.config import generate

from app.container import Container
from app.infra.config import Settings
from app.adapters.input import api
from app.adapters.input import admin


def create_lifespan(container: Container):
    @asynccontextmanager
    async def lifespan(_):
        await container.init_resources()

        client: MessageInClient = await container.scope_message_client()
        messaging_task = asyncio.tasks.create_task(with_logging(client.run))

        yield

        try:
            messaging_task.cancel()
            await messaging_task
        except asyncio.exceptions.CancelledError:
            pass

        await container.shutdown_resources()

    return lifespan


def create_app() -> FastAPI:
    settings = generate(Settings, logger)
    container = Container()
    container.config.from_pydantic(settings)
    container.wire(
        modules=[
            "app.adapters.input.admin.main",
            "app.adapters.input.api.router",
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
