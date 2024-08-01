from functools import lru_cache
import logging

from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


class Settings(BaseSettings):
    xray_executable_dir: str = Field(validation_alias="XRAY_EXECUTABLE_DIR")


@lru_cache
def get() -> Settings:
    try:
        load_dotenv(override=True)
        return BaseSettings()
    except Exception as e:
        logging.critical(f"Settings generated with error: {e}")
