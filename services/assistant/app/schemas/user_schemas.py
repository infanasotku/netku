from app.schemas.base_schema import BaseSchema, BaseSchemaPK
from app.schemas.booking_schemas import BookingAccountSchema


class UserUpdateSchema(BaseSchema):
    phone_number: str | None = None
    telegram_id: int | None = None
    proxy_subscription: bool | None = None


class UserCreateSchema(BaseSchemaPK):
    phone_number: str | None
    telegram_id: int | None

    # Subscriptions
    proxy_subscription: bool


class UserSchema(UserCreateSchema):
    booking_accounts: list[BookingAccountSchema] = []
