from app.schemas.schema import BaseSchema
from app.schemas.booking_schemas import BookingAccountSchema


class UserSchema(BaseSchema):
    phone_number: str | None
    telegram_id: int | None

    # Subscriptions
    proxy_subscription: bool

    booking_accounts: list[BookingAccountSchema] = []
