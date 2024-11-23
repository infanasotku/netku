import logging
import pathlib
import yaml


def _get_config() -> dict:
    config_path = (
        (pathlib.Path(__file__).parent / "log_config.yaml").resolve().as_posix()
    )

    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
        return config


def _create_logger(config: dict) -> logging.Logger:
    logging.config.dictConfig(config)
    return logging.getLogger("uvicorn.error")


config = _get_config()
logger = _create_logger(config)
