from pydantic import Field, computed_field
import uuid

from common.config import (
    PostgreSQLSettings,
    NetworkSettings,
    LocalAuthSettings,
    AdminSettings,
    RabbitMQSettings,
    RedisSettings,
)


class Settings(
    PostgreSQLSettings,
    NetworkSettings,
    LocalAuthSettings,
    AdminSettings,
    RabbitMQSettings,
    RedisSettings,
):
    exchange_name: str = Field(validation_alias="EXCHANGE_NAME")
    scope_routing_key: str = Field(validation_alias="SCOPE_ROUTING_KEY")

    @computed_field
    @property
    def scope_queue_name(self) -> str:
        return f"proxy_scope_{uuid.uuid4()}"

    engines_pattern: str = Field(validation_alias="ENGINES_PATTERN")
    engines_sub_channels_str: str = Field(validation_alias="ENGINES_SUB_CHANNELS")

    @computed_field
    @property
    def engines_sub_channels(self) -> list[str]:
        return self.engines_sub_channels_str.split()
