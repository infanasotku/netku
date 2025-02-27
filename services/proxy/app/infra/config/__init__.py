from pydantic import Field, computed_field
import uuid

from common.config import (
    PostgreSQLSettings,
    NetworkSettings,
    LocalAuthSettings,
    AdminSettings,
    RabbitMQSettings,
)


class Settings(
    PostgreSQLSettings,
    NetworkSettings,
    LocalAuthSettings,
    AdminSettings,
    RabbitMQSettings,
):
    exchange_name: str = Field(validation_alias="EXCHANGE_NAME")
    scope_routing_key: str = Field(validation_alias="SCOPE_ROUTING_KEY")

    @computed_field
    @property
    def scope_queue_name(self) -> str:
        return f"proxy_scope_{uuid.uuid4()}"
