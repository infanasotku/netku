from app.schemas.user_schemas import UserCreateSchema, UserSchema
from app.schemas.booking_schemas import BookingAccountCreateSchema, BookingAccountSchema

from app.database.models import BookingAccount, User


def user_create_schema_to_user(user_create: UserCreateSchema) -> User:
    return User(
        phone_number=user_create.phone_number,
        telegram_id=user_create.telegram_id,
        proxy_subscription=user_create.proxy_subscription,
    )


def user_to_user_schema(user: User) -> UserSchema:
    return UserSchema.model_validate(user)


def booking_account_create_schema_to_booking_account(
    account_create: BookingAccountCreateSchema,
) -> BookingAccount:
    return BookingAccount(
        email=account_create.email,
        password=account_create.password,
    )


def booking_account_to_booking_account_schema(
    account: BookingAccount,
) -> BookingAccountSchema:
    return BookingAccountSchema.model_validate(account)
