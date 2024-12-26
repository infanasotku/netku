from typing import Type
from sqlalchemy import inspect
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.contracts.repositories.base import BaseRepository
from app.infra.database.orm import Base


class SQLBaseRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self._session = session


def selectinload_all(model: Type[Base]):
    return [selectinload(relationship) for relationship in inspect(model).relationships]
