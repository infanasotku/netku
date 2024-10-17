from abc import ABC, abstractmethod
from typing import Any, Optional, Type

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database.database import Base
from database.models import BookingAccount, User
from database.schemas import UserSchema


class AbstractRepository(ABC):
    """Provides methods for communicating with database."""

    @abstractmethod
    def __init__(self, session: AsyncSession):
        pass

    @abstractmethod
    async def find_first(
        self,
        model: Type[Base],
        column: Any,
        value: Any,
    ) -> Optional[Base]:
        """Finds `model` row by `column == value`.
        - Returns row as `model` if it exist in DB, `None` otherwise."""
        pass

    @abstractmethod
    async def get_all(
        self,
        model: Type[Base],
    ) -> list[Base]:
        """Gets all `model` rows.
        - Returns rows as `list[model]`."""
        pass

    @abstractmethod
    async def update_user(self, user: UserSchema) -> bool:
        """Updates `user`.
        - Returns `True` if user updated, `False` otherwise."""
        pass

    @abstractmethod
    async def create_booking_account(
        self, user: UserSchema, email: str, password: str
    ) -> bool:
        """Creates new booking acccount for `user`
        Returns:
        `True` if account created successful, `False` otherwise.
        """
        pass


class Repository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_first(
        self,
        model: Type[Base],
        column: Any,
        value: Any,
    ) -> Optional[Base]:
        s = select(model).filter(column == value).options(*selectinload_all(model))
        raw = (await self.session.execute(s)).scalars().first()
        return raw

    async def get_all(self, model: Base) -> list[Base]:
        s = select(User).options(*selectinload_all(model))
        raw_users = (await self.session.execute(s)).scalars().all()
        return list(raw_users)

    async def update_user(self, user: UserSchema) -> bool:
        raw_user = await self.find_first(User, User.id, user.id)
        if raw_user is None:
            return False

        raw_user.phone_number = user.phone_number
        raw_user.telegram_id = user.telegram_id
        raw_user.proxy_subscription = user.proxy_subscription

        return True

    async def create_booking_account(
        self, user: UserSchema, email: str, password: str
    ) -> bool:
        raw_user = await self.find_first(User, User.id, user.id)
        if raw_user is None:
            return False

        booking_account = BookingAccount(email=email, password=password, owner=raw_user)

        await self.session.add(booking_account)

        return True


def selectinload_all(model: Type[Base]):
    return [selectinload(relationship) for relationship in inspect(model).relationships]
