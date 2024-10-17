from abc import ABC, abstractmethod
from typing import Any, Optional, Type

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database.database import Base
from database.models import User
from database.schemas import BaseSchema


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
        q = select(model).filter(column == value).options(*selectinload_all(model))
        raw = (await self.session.execute(q)).first()
        return schema.model_validate(raw) if raw is not None else None

    async def get_all(self, schema: BaseSchema, model: Base) -> list[BaseSchema]:
        q = select(User).options(*selectinload_all(model))
        raw_users = (await self.session.execute(q)).scalars().all()
        return [schema.model_validate(raw_user) for raw_user in raw_users]


def selectinload_all(model: Type[Base]):
    return [selectinload(relationship) for relationship in inspect(model).relationships]
