from fastapi import FastAPI
import uvicorn

from common.logging import config, logger
from common.config import generate

from dependencies import AuthDependencies
from app.infra.config import Settings

from app.adapters.input.admin import register_admin
from app.adapters.input import api


def run():
    settings = generate(Settings, logger)
    dependencies = AuthDependencies(settings, logger)

    app = FastAPI()
    register_admin(
        app,
        engine=dependencies.sql_connection.async_engine,
        username=settings.admin_username,
        password=settings.admin_password,
        create_security_client=dependencies.create_security_client,
    )
    app.mount("/api", api.create_api(dependencies.create_client_service))

    uvicorn.run(
        app=app,
        host=settings.host,
        port=settings.port,
        log_config=config,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
    )


if __name__ == "__main__":
    run()
