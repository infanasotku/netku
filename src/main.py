from configure import configure
import settings
import uvicorn
import xray


def run():
    configure()
    settings.get()

    log_config_path = settings.get().app_directory_path + "/log_config.yaml"
    uvicorn.run(
        app=xray.create(),
        host=settings.get().host,
        port=settings.get().port,
        log_config=log_config_path,
    )


if __name__ == "__main__":
    run()
