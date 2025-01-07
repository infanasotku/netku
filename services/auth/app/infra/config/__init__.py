from pydantic import Field
from common.config import PostgreSQLSettings, NetworkSettings, AdminSettings


class Settings(PostgreSQLSettings, NetworkSettings, AdminSettings):
    jwt_secret: str = Field(validation_alias="JWT_SECRET")
