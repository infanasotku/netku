import logging
import pathlib
import sys
from typing import Optional
import uuid

from pydantic_settings import BaseSettings
from pydantic import Field, computed_field
from dotenv import load_dotenv


class Settings(BaseSettings):
    # region Network
    host: str = Field(validation_alias="HOST", default="127.0.0.1")
    port: int = Field(validation_alias="PORT", default=5100)
    domain: str = Field(validation_alias="DOMAIN", default="127.0.0.1")
    ssl_keyfile: Optional[str] = Field(validation_alias="SSL_KEYFILE", default=None)
    ssl_certfile: Optional[str] = Field(validation_alias="SSL_CERTFILE", default=None)
    # endregion

    # region Xray
    xray_restart_minutes: float = Field(validation_alias="XRAY_RESTART_MINUTES")
    xray_port: int = Field(validation_alias="XRAY_PORT", default=9000)
    xray_host: str = Field(validation_alias="XRAY_HOST", default="127.0.0.1")
    # endregion

    # region Bot
    bot_token: str = Field(validation_alias="BOT_TOKEN")
    telegram_token: str = Field(
        validation_alias="TELEGRAM_TOKEN", default=str(uuid.uuid4())
    )
    bot_webhook_url: str = Field(validation_alias="BOT_WEBHOOK_URL")
    # endregion

    # region psql
    psql_pass: str = Field(validation_alias="POSTGRES_PASSWORD")
    psql_user: str = Field(validation_alias="POSTGRES_USER")
    psql_host: str = Field(validation_alias="POSTGRES_HOST", default="127.0.0.1")
    psql_port: int = Field(validation_alias="POSTGRES_PORT", default=5432)
    psql_db_name: str = Field(validation_alias="POSTGRES_DB_NAME", default="postgres")

    @computed_field
    @property
    def psql_dsn(self) -> str:
        return (
            f"postgresql+psycopg://{self.psql_user}:{self.psql_pass}"
            + f"@{self.psql_host}:{self.psql_port}/{self.psql_db_name}"
        )

    # endregion

    @computed_field
    @property
    def app_directory_path(self) -> str:
        return (pathlib.Path(__file__).parent).resolve().as_posix()


def _generate() -> Settings:
    """Gets cached settings of app."""
    try:
        load_dotenv(override=True)
        return Settings()
    except Exception as e:
        logging.critical(f"Settings generated with error: {e}")
        sys.exit(1)


settings = _generate()
logger = logging.getLogger("uvicorn.error")
