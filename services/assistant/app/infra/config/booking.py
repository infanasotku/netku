from pydantic_settings import BaseSettings
from pydantic import Field


class BookingSettings(BaseSettings):
    booking_port: int = Field(validation_alias="BOOKING_PORT", default=9001)
    booking_host: str = Field(validation_alias="BOOKING_HOST", default="127.0.0.1")
