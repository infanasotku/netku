import sys
import os

from pydantic import Field, computed_field
from dotenv import load_dotenv

from app.infra.logging.logger import logger

from app.infra.config.booking import BookingSettings
from app.infra.config.bot import BotSettings
from app.infra.config.postgres import PostgreSQLSettings
from app.infra.config.xray import XraySettings
from app.infra.config.mongo import MongoSettings
from app.infra.config.rabbitmq import RabbitMQSettings


class Settings(
    XraySettings,
    BookingSettings,
    BotSettings,
    PostgreSQLSettings,
    MongoSettings,
    RabbitMQSettings,
):
    # region Network
    host: str = Field(validation_alias="ASSISTANT_HOST", default="127.0.0.1")
    port: int = Field(validation_alias="ASSISTANT_PORT", default=5100)
    domain: str = Field(validation_alias="DOMAIN", default="127.0.0.1")
    ssl_keyfile: str | None = Field(validation_alias="SSL_KEYFILE", default=None)
    ssl_certfile: str | None = Field(validation_alias="SSL_CERTFILE", default=None)

    @computed_field
    @property
    def app_directory_path(self) -> str:
        return os.getcwd()


def _generate() -> Settings:
    """Gets cached settings of app."""
    try:
        load_dotenv(override=True)
        return Settings()
    except Exception as e:
        logger.critical(f"Settings generated with error: {e}")
        sys.exit(1)


settings = _generate()
