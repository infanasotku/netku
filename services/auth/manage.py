from fastapi import FastAPI
import uvicorn

from common.logging import config, logger
from common.config import generate

from dependencies import AuthDependencies
from app.infra.config import Settings


def run():
    settings = generate(Settings, logger)
    dependencies = AuthDependencies(settings, logger)

    uvicorn.run(
        app=FastAPI(),
        host=settings.host,
        port=settings.port,
        log_config=config,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
    )


if __name__ == "__main__":
    run()
