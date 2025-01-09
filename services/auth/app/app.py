from fastapi import FastAPI

from common.logging import logger
from common.config import generate

from app.container import Container
from app.infra.config import Settings
from app.adapters.input import api
from app.adapters.input.admin import register_admin


def create_app() -> FastAPI:
    settings = generate(Settings, logger)
    container = Container()
    container.config.from_pydantic(settings)
    container.wire(
        modules=[
            "app.adapters.input.api.auth.token.router",
            "app.adapters.input.admin.views",
            "app.adapters.input.admin.main",
            "app.adapters.input.api.dependencies",
        ]
    )

    app = FastAPI(redoc_url=None, docs_url=None)
    register_admin(
        app,
        username=settings.admin_username,
        password=settings.admin_password,
    )
    app.mount("/api", api.create_api())

    return app


app = create_app()
