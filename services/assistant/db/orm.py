from typing import Any, Optional
from db.database import Base, engine, session

from db.schemas import UserSchema
from db.models import User, BookingAccount


def create_tables():
    Base.metadata.create_all(engine)


def get_user(column: Any, value: Any) -> Optional[UserSchema]:
    """Returns user by `column == value`.
    - Returns `UserSchema` if he exist in db, `None` otherwise."""
    with session.begin() as s:
        raw_user = s.query(User).filter(column == value).first()
        if not raw_user:
            return

        return UserSchema.model_validate(raw_user)


def update_user(new_user: UserSchema) -> bool:
    """Updates user.
    - Returns `True` if user updated, `False` otherwise."""
    with session.begin() as s:
        raw_user = s.query(User).filter(User.id == new_user.id).first()
        if not raw_user:
            return

        raw_user.phone_number = new_user.phone_number
        raw_user.telegram_id = new_user.telegram_id
        raw_user.proxy_subscription = new_user.proxy_subscription

        raw_user.booking_accounts = []

        for booking_account in new_user.booking_accounts:
            raw_booking_accoount = (
                s.query(BookingAccount)
                .filter(BookingAccount.id == booking_account.id)
                .first()
            )
            raw_user.booking_accounts.append(raw_booking_accoount)

    return True


def get_users() -> list[UserSchema]:
    """Returns all user in db."""
    with session.begin() as s:
        raw_users = s.query(User).all()

        return [UserSchema.model_validate(raw_user) for raw_user in raw_users]
