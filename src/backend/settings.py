from functools import cache
import logging
import pathlib
import sys
import json
from typing import Optional

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
    xray_executable_dir: str = Field(validation_alias="XRAY_EXECUTABLE_DIR")
    xray_executable_name: str = Field(validation_alias="XRAY_EXECUTABLE_NAME")
    xray_restart_minutes: float = Field(validation_alias="XRAY_RESTART_MINUTES")
    xray_fallback: str = Field(validation_alias="XRAY_FALLBACK")

    @computed_field
    @property
    def xray_config(self) -> dict:
        try:
            logging.info("Loading xray config")
            with open(f"{self.app_directory_path}/xray/xray_config.json", "r") as f:
                config = json.loads(f.read())
                logging.info("Xray config loaded")
                return config
        except Exception as e:
            logging.critical(f"Xray config loaded with error: {e}")
            sys.exit(1)

    # endregion

    @computed_field
    @property
    def app_directory_path(self) -> str:
        return (pathlib.Path(__file__).parent).resolve().as_posix()


@cache
def get() -> Settings:
    try:
        load_dotenv(override=True)
        return Settings()
    except Exception as e:
        logging.critical(f"Settings generated with error: {e}")
        sys.exit(1)
