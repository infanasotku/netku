from pydantic import Field

from common.config import (
    PostgreSQLSettings,
    NetworkSettings,
    AdminSettings,
    LocalAuthSettings,
    RabbitMQSettings,
)


class Settings(
    PostgreSQLSettings,
    NetworkSettings,
    AdminSettings,
    LocalAuthSettings,
    RabbitMQSettings,
):
    rabbit_vhost: str = Field(validation_alias="RABBITMQ_VHOST", default="/")
    scope_routing_key: str = Field(validation_alias="SCOPE_ROUTING_KEY")
    scope_exchange_name: str = Field(validation_alias="SCOPE_EXCHANGE_NAME")
