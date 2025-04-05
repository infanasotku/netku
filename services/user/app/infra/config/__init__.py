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
    rabbit_vhost: str = Field(validation_alias="RABBITMQ_VHOST", default="/")

    scope_exchange_name: str = Field(validation_alias="SCOPE_EXCHANGE_NAME")
    scope_routing_key: str = Field(validation_alias="SCOPE_ROUTING_KEY")

    @computed_field
    @property
    def scope_queue_name(self) -> str:
        return f"user_{uuid.uuid4()}"
