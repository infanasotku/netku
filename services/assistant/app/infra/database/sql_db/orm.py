from typing import Type, TypeAlias

from sqlalchemy import inspect
from sqlalchemy.orm import selectinload

from contextlib import asynccontextmanager
from typing import Annotated, AsyncContextManager, Callable

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    id: Mapped[intpk]


GetSQLDB: TypeAlias = Callable[[], AsyncContextManager[AsyncSession]]


def get_db_factory(
    async_session: async_sessionmaker[AsyncSession],
) -> GetSQLDB:
    @asynccontextmanager
    async def get_db():
        async with async_session.begin() as session:
            yield session

    return get_db


def selectinload_all(model: Type[Base]):
    return [selectinload(relationship) for relationship in inspect(model).relationships]
