from typing import Optional
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

    id: Optional[int] = -1


class UserSchema(BaseSchema):
    phone_number: Optional[str]
    telegram_id: Optional[int]

    # Subscriptions
    proxy_subscription: bool

    booking_accounts: list["BookingAccountSchema"] = []


class BookingAccountSchema(BaseSchema):
    email: str
    password: str
