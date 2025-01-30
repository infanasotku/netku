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
    scopes_routing_key: str = Field(validation_alias="SCOPES_ROUTING_KEY")
