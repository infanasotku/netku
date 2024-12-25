import sys
import os

from pydantic import Field, computed_field
from dotenv import load_dotenv

from app.infra.logging.logger import logger

from app.infra.config.postgres import PostgreSQLSettings


class Settings(PostgreSQLSettings):
    # region Network
    host: str = Field(validation_alias="HOST", default="127.0.0.1")
    port: int = Field(validation_alias="PORT", default=5100)
    ssl_keyfile: str | None = Field(validation_alias="SSL_KEYFILE", default=None)
    ssl_certfile: str | None = Field(validation_alias="SSL_CERTFILE", default=None)

    @computed_field
    @property
    def app_directory_path(self) -> str:
        return os.getcwd()


def _generate() -> Settings:
    try:
        load_dotenv(override=True)
        return Settings()
    except Exception as e:
        logger.critical(f"Settings generated with error: {e}")
        sys.exit(1)


settings = _generate()
