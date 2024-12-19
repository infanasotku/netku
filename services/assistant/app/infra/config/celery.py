from pydantic_settings import BaseSettings
from pydantic import Field


class CelerySettings(BaseSettings):
    concurrency: int = Field(validation_alias="CONCURRENCY", default=1)
