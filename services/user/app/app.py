from fastapi import FastAPI

from common.logging import logger
from common.config import generate

from app.container import Container
from app.infra.config import Settings
from app.adapters.input import api


def create_app() -> FastAPI:
    settings = generate(Settings, logger)
    container = Container()
    container.config.from_pydantic(settings)
    container.wire(
        modules=[
            "app.adapters.input.api.router",
        ]
    )

    app = FastAPI()
    app.container = container
    app.mount("/api", api.create_api())

    return app


app = create_app()
