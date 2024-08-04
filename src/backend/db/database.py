from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from settings import settings


engine = create_engine(settings.psql_dsn)

session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
