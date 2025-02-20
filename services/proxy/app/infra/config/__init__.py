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
    scope_exchange_name: str = Field(validation_alias="SCOPE_EXCHANGE_NAME")
    scope_routing_key: str = Field(validation_alias="SCOPE_ROUTING_KEY")

    @computed_field
    @property
    def scope_queue_name(self) -> str:
        return f"proxy_{uuid.uuid4()}"

    xray_host: str = Field(validate_default="XRAY_HOST")
    xray_port: str = Field(validate_default="XRAY_PORT")
