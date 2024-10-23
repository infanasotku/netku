from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = -1


class UserSchema(BaseSchema):
    phone_number: str | None
    telegram_id: int | None

    # Subscriptions
    proxy_subscription: bool

    booking_accounts: list["BookingAccountSchema"] = []


class BookingAccountSchema(BaseSchema):
    email: str
    password: str
