from abc import ABC
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, Optional

from database.models import BookingAccount, User
from database.orm import AbstractRepository, Repository
from database.schemas import BookingAccountSchema, UserSchema


class ServiceFactory:
    """Specifies factory for DB services."""

    def __init__(self, get_db: Callable):
        self.get_db = get_db

    @asynccontextmanager
    async def user_service_factory(self) -> AsyncGenerator["UserService", None]:
        async with self.get_db() as session:
            yield UserService(Repository(session))

    @asynccontextmanager
    async def booking_service_factory(self) -> AsyncGenerator["BookingService", None]:
        async with self.get_db() as session:
            yield BookingService(Repository(session))


class AbstractService(ABC):
    def __init__(self, repository: AbstractRepository):
        self.repository = repository


class UserService(AbstractService):
    async def get_user_by_telegram_id(self, id: int) -> Optional[UserSchema]:
        """Gets user by `UserSchema.telegram_id`.
        - Returns user as `UserSchema` if it exist in db, `None` otherwise."""
        user = await self.repository.find_first(User, User.telegram_id, id)
        return UserSchema.model_validate(user) if user is not None else None

    async def get_user_by_phone(self, phone: str) -> Optional[UserSchema]:
        """Gets user by `UserSchema.phone_number`.
        - Returns user as `UserSchema` if it exist in db, `None` otherwise."""
        return [
            UserSchema.model_validate(user)
            for user in await self.repository.find_first(
                UserSchema, User, User.phone_number, phone
            )
        ]

    async def get_users(self) -> list[UserSchema]:
        """Returns all user in db."""
        return [
            UserSchema.model_validate(user)
            for user in await self.repository.get_all(User)
        ]

    async def update_user(self, user: UserSchema) -> bool:
        """Updates user.
        - Returns `True` if user updated, `False` otherwise."""

        return await self.repository.update_user(user)


class BookingService(AbstractService):
    async def create_booking_account(
        self, user: UserSchema, email: str, password: str
    ) -> bool:
        return await self.repository.create_booking_account(user, email, password)

    async def get_booking_account_by_id(
        self, id: int
    ) -> Optional[BookingAccountSchema]:
        """Returns booking account by `id`."""
        account = await self.repository.find_first(
            BookingAccount, BookingAccount.id, id
        )
        return (
            BookingAccountSchema.model_validate(account)
            if account is not None
            else None
        )
