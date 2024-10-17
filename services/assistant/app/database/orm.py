from abc import ABC, abstractmethod
from typing import Any, Optional, Type

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database.database import Base
from database.models import User
from database.schemas import BaseSchema, UserSchema


class AbstractRepository(ABC):
    """Provides methods for communicating with database."""

    @abstractmethod
    def __init__(self, session: AsyncSession):
        pass

    @abstractmethod
    async def find_first(
        self,
        schema: Type[BaseSchema],
        model: Type[Base],
        column: Any,
        value: Any,
    ) -> Optional[BaseSchema]:
        """Finds `model` row by `column == value`.
        - Returns row as `schema_type` if it exist in db, `None` otherwise."""
        pass

    @abstractmethod
    async def get_all(
        self,
        schema: Type[BaseSchema],
        model: Type[Base],
    ) -> list[BaseSchema]:
        """Gets all `model` rows.
        - Returns rows as `list[schema_type]`."""
        pass

    @abstractmethod
    async def update_user(self, new_user: UserSchema) -> bool:
        """Updates user.
        - Note: Row in DB must be update manually with `session.flush()` or `session.close` etc.
        - Returns `True` if user updated, `False` otherwise."""
        pass


class Repository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_first(
        self,
        schema: Type[BaseSchema],
        model: Type[Base],
        column: Any,
        value: Any,
    ) -> Optional[BaseSchema]:
        s = select(model).filter(column == value).options(*selectinload_all(model))
        raw = (await self.session.execute(s)).scalar().first()
        return schema.model_validate(raw) if raw is not None else None

    async def get_all(self, schema: BaseSchema, model: Base) -> list[BaseSchema]:
        s = select(User).options(*selectinload_all(model))
        raw_users = (await self.session.execute(s)).scalars().all()
        return [schema.model_validate(raw_user) for raw_user in raw_users]

    async def update_user(self, new_user: UserSchema) -> bool:
        s = select(User).filter(User.id == new_user.id).options(*selectinload_all(User))
        raw_user = (await self.session.execute(s)).scalars().first()
        if not raw_user:
            return False

        raw_user.phone_number = new_user.phone_number
        raw_user.telegram_id = new_user.telegram_id
        raw_user.proxy_subscription = new_user.proxy_subscription
        return True


def selectinload_all(model: Type[Base]):
    return [selectinload(relationship) for relationship in inspect(model).relationships]
