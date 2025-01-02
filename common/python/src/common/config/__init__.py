import sys
from logging import Logger
from typing import Type, TypeVar
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from common.config.postgres import PostgreSQLSettings
from common.config.network import NetworkSettings


SettingsT = TypeVar("SettingsT", bound=BaseSettings)


def generate(SettingsClass: Type[SettingsT], logger: Logger) -> SettingsT:
    try:
        load_dotenv(override=True)
        return SettingsClass()
    except Exception as e:
        logger.critical(f"Settings generated with error: {e}")
        sys.exit(1)


__all__ = ["NetworkSettings", "PostgreSQLSettings"]
