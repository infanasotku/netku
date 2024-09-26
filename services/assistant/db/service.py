from typing import Optional
from db import orm
from db.schemas import UserSchema, BookingAccountSchema
from db.models import BookingAccount, User
from settings import logger


def get_user_by_telegram_id(id: int) -> Optional[UserSchema]:
    """Returns user by `UserSchema.telegram_id`.
    - Returns `UserSchema` if he exist in db, `None` otherwise."""
    return orm.get_schema(UserSchema, User, User.telegram_id, id)


def get_user_by_phone(phone: str) -> Optional[UserSchema]:
    """Returns user by `UserSchema.phone_number`.
    - Returns `UserSchema` if he exist in db, `None` otherwise."""
    return orm.get_user(UserSchema, User, User.phone_number, phone)


def update_user(user: UserSchema):
    """Updates user."""

    if not orm.update_user(user):
        logger.warning("User updating failed.")


def get_users() -> list[UserSchema]:
    """Returns all user in db."""
    users = orm.get_users()

    if not users:
        logger.warning("User table is empty.")

    return users


def create_booking_account(user: UserSchema, email: str, password: str):
    if not orm.create_booking_account(user, email, password):
        logger.warning("Booking account not created")


def get_booking_account_by_id(id: int) -> Optional[BookingAccountSchema]:
    """Returns booking account by `id`."""
    return orm.get_schema(BookingAccountSchema, BookingAccount, BookingAccount.id, id)
