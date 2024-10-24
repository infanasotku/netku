from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Type, TypeVar

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.database import Base
from app.database.models import BookingAccount, User, XrayRecord
from app.database.schemas import UserSchema


ModelT = TypeVar("ModelT", bound=Base)


class AbstractRepository(ABC):
    """Provides methods for communicating with database."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_changes(self):
        await self.session.flush()

    @abstractmethod
    async def find_first(
        self,
        model: Type[ModelT],
        column: Any,
        value: Any,
    ) -> ModelT | None:
        """Finds `model` row by `column == value`.

        :return: Row as `model` if it exist in DB, `None` otherwise."""

    @abstractmethod
    async def get_all(
        self,
        model: Type[ModelT],
    ) -> list[ModelT]:
        """Gets all `model` rows.

        :return: Rows as `list[model]`."""

    @abstractmethod
    async def update_user(self, user: UserSchema) -> bool:
        """Updates `user`.

        :return: `True` if user updated, `False` otherwise."""

    @abstractmethod
    async def create_booking_account(
        self, user: UserSchema, email: str, password: str
    ) -> bool:
        """Creates new booking acccount for `user`

        :return: `True` if account created successful, `False` otherwise.
        """

    @abstractmethod
    async def update_xray_record(self, uid: str) -> None:
        """Saves xray uid in DB."""

    @abstractmethod
    async def get_xray_record(self) -> XrayRecord | None:
        """Gets xray record from DB."""


class Repository(AbstractRepository):
    async def find_first(
        self,
        model: Type[ModelT],
        column: Any,
        value: Any,
    ) -> ModelT | None:
        s = select(model).filter(column == value).options(*selectinload_all(model))
        raw = (await self.session.execute(s)).scalars().first()
        return raw

    async def get_all(self, model: Type[ModelT]) -> list[ModelT]:
        s = select(model).options(*selectinload_all(model))
        raw_models = (await self.session.execute(s)).scalars().all()
        return list(raw_models)

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

        self.session.add(booking_account)

        return True

    async def update_xray_record(self, uid: str) -> None:
        xray_record = XrayRecord(uid=uid, last_update=datetime.now())
        xray_records = await self.get_all(XrayRecord)

        if len(xray_records) == 0:
            self.session.add(xray_record)
        else:
            xray_records[0].uid = xray_record.uid
            xray_records[0].last_update = xray_record.last_update

    async def get_xray_record(self) -> XrayRecord | None:
        xray_records = await self.get_all(XrayRecord)

        if len(xray_records) > 0:
            return xray_records[0]


def selectinload_all(model: Type[Base]):
    return [selectinload(relationship) for relationship in inspect(model).relationships]
