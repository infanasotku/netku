from pydantic_settings import BaseSettings
from pydantic import Field


class AdminSettings(BaseSettings):
    username: str = Field(validation_alias="ADMIN_USERNAME")
    password: int = Field(validation_alias="ADMIN_PASSWORD")
