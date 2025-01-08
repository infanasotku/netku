from fastapi import FastAPI
import uvicorn

from common.logging import config, logger
from common.config import generate

from app.container import Container

from app.infra.config import Settings

from app.adapters.input.admin import register_admin
from app.adapters.input import api


def run():
    settings = generate(Settings, logger)
    container = Container()
    container.config.from_pydantic(settings)
    container.wire(
        modules=[
            "app.adapters.input.api.auth.token",
            "app.adapters.input.admin.views",
            "app.adapters.input.admin.main",
        ]
    )

    app = FastAPI(redoc_url=None, docs_url=None)
    register_admin(
        app,
        username=settings.admin_username,
        password=settings.admin_password,
    )
    app.mount("/api", api.create_api())

    uvicorn.run(
        app=app,
        host=settings.host,
        port=settings.port,
        log_config=config,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
        root_path=settings.root_path,
    )


if __name__ == "__main__":
    run()
