import uvicorn

from app.infra.config import settings
from app.infra.logging import config, logger

from dependencies import UserDependencies

import app
from app.adapters.input import api


def run():
    dependencies = UserDependencies(settings, logger)

    sub_apps = (
        app.AppConfig(api.create_api(dependencies.create_user_service), "/api"),
    )

    uvicorn.run(
        app=app.create_app(sub_apps),
        host=settings.host,
        port=settings.port,
        log_config=config,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
    )


if __name__ == "__main__":
    run()
