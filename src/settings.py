from functools import lru_cache
import logging
import pathlib
import sys

from pydantic_settings import BaseSettings
from pydantic import Field, computed_field
from dotenv import load_dotenv


class Settings(BaseSettings):
    host: str = Field(validation_alias="HOST", default="127.0.0.1")
    port: int = Field(validation_alias="PORT", default=5100)

    xray_executable_dir: str = Field(validation_alias="XRAY_EXECUTABLE_DIR")

    @computed_field
    @property
    def app_directory_path(self) -> str:
        return (pathlib.Path(__file__).parent).resolve().as_posix()


@lru_cache
def get() -> Settings:
    try:
        load_dotenv(override=True)
        return Settings()
    except Exception as e:
        logging.critical(f"Settings generated with error: {e}")
        sys.exit(1)
