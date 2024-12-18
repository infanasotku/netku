from typing import Type, TypeAlias

from sqlalchemy import inspect
from sqlalchemy.orm import selectinload

from typing import Annotated, AsyncContextManager, Callable

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    id: Mapped[intpk]


GetSQLDB: TypeAlias = Callable[[], AsyncContextManager[AsyncSession]]


def selectinload_all(model: Type[Base]):
    return [selectinload(relationship) for relationship in inspect(model).relationships]
