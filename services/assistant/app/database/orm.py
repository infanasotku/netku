from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.database import Base
from app.database.models import XrayRecord


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
    async def create(self, entity: ModelT) -> ModelT:
        """Creates `entity` in DB.

        :return: Created row.
        """

    @abstractmethod
    async def update(self, entity: ModelT) -> None:
        """Update `entity` in DB."""

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

    async def create(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)

        return entity

    async def update(self, entity: ModelT) -> ModelT:
        await self.session.flush()
        await self.session.refresh(entity)

    async def get_xray_record(self) -> XrayRecord | None:
        xray_records = await self.get_all(XrayRecord)

        if len(xray_records) > 0:
            return xray_records[0]


def selectinload_all(model: Type[Base]):
    return [selectinload(relationship) for relationship in inspect(model).relationships]
