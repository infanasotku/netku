from typing import TypeAlias


from typing import Annotated, AsyncContextManager, Callable

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


intpk = Annotated[int, mapped_column(primary_key=True)]
GetSQLDB: TypeAlias = Callable[[], AsyncContextManager[AsyncSession]]


class Base(DeclarativeBase):
    id: Mapped[intpk]
