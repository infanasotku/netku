from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from settings import settings


engine = create_engine(settings.psql_dsn)

session = sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    id: Mapped[intpk]
