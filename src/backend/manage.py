import uvicorn
from configure import configure
from core import create
from settings import settings


def run():
    configure()

    log_config_path = settings.app_directory_path + "/log_config.yaml"
    uvicorn.run(
        app=create(),
        host=settings.host,
        port=settings.port,
        log_config=log_config_path,
        ssl_keyfile=settings.ssl_keyfile,
        ssl_certfile=settings.ssl_certfile,
    )


if __name__ == "__main__":
    run()
