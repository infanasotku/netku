import uvicorn

from app.infra.config import settings
from app.infra.logging import config

import app
from app.adapters.input import api


def run():
    sub_apps = (app.AppConfig(api.create_api(), "/user"),)

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
