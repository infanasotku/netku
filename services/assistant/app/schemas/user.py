from enum import Enum
from pydantic import field_validator

from app.schemas.base import BaseSchema, BaseSchemaPK
from app.schemas.booking import BookingAccountSchema


class Subscription(Enum):
    proxy_subscription = 1
    availability_subscription = 2


class UserUpdateSchema(BaseSchema):
    phone_number: str | None = None
    telegram_id: int | None = None
    proxy_subscription: bool | None = None
    availability_subscription: bool | None = None


class UserCreateSchema(BaseSchemaPK):
    phone_number: str | None
    telegram_id: int | None

    # Subscriptions
    proxy_subscription: bool
    availability_subscription: bool

    @field_validator("availability_subscription", mode="before")
    @classmethod
    def upload_file_validate(cls, val):
        if val is None:
            return False
        else:
            return val


class UserSchema(UserCreateSchema):
    booking_accounts: list[BookingAccountSchema] = []
