from typing import Any, Optional, Type
from db.database import Base, engine, session

from db.schemas import UserSchema, BaseSchema
from db.models import User, BookingAccount


def create_tables():
    Base.metadata.create_all(engine)


def get_schema(
    schema_type: Type[BaseSchema], model_type: Type[Base], column: Any, value: Any
) -> Optional[BaseSchema]:
    """Returns schemas by `column == value`.
    - Returns `schema_type` if he exist in db, `None` otherwise."""
    with session.begin() as s:
        raw = s.query(model_type).filter(column == value).first()
        if not raw:
            return

        return schema_type.model_validate(raw)


def update_user(new_user: UserSchema) -> bool:
    """Updates user.
    - Returns `True` if user updated, `False` otherwise."""
    with session.begin() as s:
        raw_user = s.query(User).filter(User.id == new_user.id).first()
        if not raw_user:
            return False

        raw_user.phone_number = new_user.phone_number
        raw_user.telegram_id = new_user.telegram_id
        raw_user.proxy_subscription = new_user.proxy_subscription

    return True


def get_users() -> list[UserSchema]:
    """Returns all user in db."""
    with session.begin() as s:
        raw_users = s.query(User).all()

        return [UserSchema.model_validate(raw_user) for raw_user in raw_users]


def create_booking_account(user: UserSchema, email: str, password: str) -> bool:
    """Creates new booking acccount for `user`
    Returns:
    `True` if account created successful, `False` otherwise.
    """
    with session.begin() as s:
        raw_user = s.query(User).filter(User.id == user.id).first()
        if not raw_user:
            return False

        booking_account = BookingAccount(email=email, password=password, owner=raw_user)

        s.add(booking_account)

    return True
