from pydantic_settings import BaseSettings
from pydantic import Field


class XraySettings(BaseSettings):
    xray_port: int = Field(validation_alias="XRAY_PORT", default=9000)
    xray_host: str = Field(validation_alias="XRAY_HOST", default="127.0.0.1")
