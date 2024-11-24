from app.schemas.user import UserCreateSchema, UserSchema
from app.schemas.booking import BookingAccountCreateSchema, BookingAccountSchema
from app.schemas.xray import XrayRecordCreateSchema, XrayRecordSchema

from app.infra.database.sql_db.models import BookingAccount, User, XrayRecord


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
        owner_id=account_create.owner_id,
        email=account_create.email,
        password=account_create.password,
    )


def booking_account_to_booking_account_schema(
    account: BookingAccount,
) -> BookingAccountSchema:
    return BookingAccountSchema.model_validate(account)


def xray_record_to_xray_record_schema(
    xray_record: XrayRecord,
) -> XrayRecordSchema:
    return XrayRecordSchema.model_validate(xray_record)


def xray_record_create_schema_to_xray_record(
    xray_record_create: XrayRecordCreateSchema,
) -> BookingAccount:
    return XrayRecord(
        uid=xray_record_create.uid,
        last_update=xray_record_create.last_update,
    )
