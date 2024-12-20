from pydantic_settings import BaseSettings
from pydantic import Field


class RabbitMQSettings(BaseSettings):
    rabbit_user: str = Field(validation_alias="RABBITMQ_DEFAULT_USER")
    rabbit_pass: str = Field(validation_alias="RABBITMQ_DEFAULT_PASS")
    rabbit_host: str = Field(validation_alias="RABBITMQ_HOST", default="127.0.0.1")
    rabbit_port: int = Field(validation_alias="RABBITMQ_PORT", default=5672)
