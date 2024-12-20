import logging
import logging.config
import pathlib
import re
import yaml
from uvicorn.logging import DefaultFormatter


class AppFormatter(DefaultFormatter):
    CYAN = "\033[96m"
    RESET = "\033[0m"

    def formatMessage(self, record):
        msg = super().formatMessage(record)

        words = msg.split(" ")

        for index, word in enumerate(words):
            if "\033[" not in word:
                words[index] = re.sub(
                    r"\[([^\s\[\]]+)\]", rf"[{self.CYAN}\1{self.RESET}]", word
                )

        return " ".join(words)


def _get_config() -> dict:
    config_path = (
        (pathlib.Path(__file__).parent / "log_config.yaml").resolve().as_posix()
    )

    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
        config["formatters"]["default"]["()"] = AppFormatter
        return config


def _create_logger(config: dict) -> logging.Logger:
    logging.config.dictConfig(config)
    return logging.getLogger("uvicorn")


config = _get_config()
logger = _create_logger(config)
