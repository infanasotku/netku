import uvicorn

from common.logging import config, logger
from common.config import generate

from dependencies import UserDependencies
from app.infra.config import Settings

from app.adapters.input import api


def run():
    settings = generate(Settings, logger)
    dependencies = UserDependencies(settings, logger)

    uvicorn.run(
        app=api.create_api(dependencies.create_user_service),
        host=settings.host,
        port=settings.port,
        log_config=config,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
    )


if __name__ == "__main__":
    run()
