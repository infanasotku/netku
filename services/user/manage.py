import uvicorn

from app.infra.config import settings
from app.infra.logging import config
import app


def run():
    uvicorn.run(
        app=app.create_app(),
        host=settings.host,
        port=settings.port,
        log_config=config,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
    )


if __name__ == "__main__":
    run()
