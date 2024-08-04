import logging
import settings


def configure():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:     [%(asctime)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )
    settings.get()
