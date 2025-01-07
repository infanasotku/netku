from fastapi import FastAPI
import uvicorn

from common.logging import config, logger
from common.config import generate

from dependencies import UserDependencies
from app.infra.config import Settings

from app.adapters.input import api


def run():
    settings = generate(Settings, logger)
    dependencies = UserDependencies(settings, logger)

    app = FastAPI()
    app.mount("/api", api.create_api(dependencies.create_user_service))

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
