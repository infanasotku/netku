from pydantic_settings import BaseSettings
from pydantic import Field


class AdminSettings(BaseSettings):
    admin_username: str = Field(validation_alias="ADMIN_USERNAME")
    admin_password: int = Field(validation_alias="ADMIN_PASSWORD")
