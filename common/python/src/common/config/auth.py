from pydantic_settings import BaseSettings
from pydantic import Field


class AuthSettings(BaseSettings):
    auth_url: str = Field(validation_alias="AUTH_URL")
    client_id: str = Field(validation_alias="CLIENT_ID")
    client_secret: str = Field(validation_alias="CLIENT_SECRET")
    with_auth_ssl: bool = Field(validation_alias="WITH_AUTH_SSL", default=True)
