from pydantic_settings import BaseSettings
from pydantic import Field


class RedisSettings(BaseSettings):
    redis_pass: str | None = Field(validation_alias="REDIS_PASS", default=None)
    redis_host: str = Field(validation_alias="REDIS_HOST", default="127.0.0.1")
    redis_port: int = Field(validation_alias="REDIS_PORT", default=5672)
