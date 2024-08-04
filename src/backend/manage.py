import uvicorn
from configure import configure
from core import create
import settings


def run():
    configure()

    log_config_path = settings.get().app_directory_path + "/log_config.yaml"
    uvicorn.run(
        app=create(),
        host=settings.get().host,
        port=settings.get().port,
        log_config=log_config_path,
        ssl_keyfile=settings.get().ssl_keyfile,
        ssl_certfile=settings.get().ssl_certfile,
    )


if __name__ == "__main__":
    run()
