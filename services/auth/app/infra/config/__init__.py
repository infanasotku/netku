from pydantic import Field
from common.config import PostgreSQLSettings, NetworkSettings, AdminSettings


class Settings(PostgreSQLSettings, NetworkSettings, AdminSettings):
    secret: str = Field(validation_alias="SECRET")
