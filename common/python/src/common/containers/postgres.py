from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager

from common.containers.base import BaseContainer


@asynccontextmanager
async def get_session(async_sessionmaker: async_sessionmaker):
    async with async_sessionmaker.begin() as session:
        yield session


@containers.copy(BaseContainer)
class PostgresContainer(BaseContainer):
    async_engine = providers.Singleton(
        create_async_engine,
        BaseContainer.config.psql_dsn,
        connect_args=providers.Dict(
            server_settings=providers.Dict(search_path=BaseContainer.config.psql_schema)
        ),
    )
    async_sessionmaker = providers.Singleton(async_sessionmaker, async_engine)

    session = providers.Factory(get_session, async_sessionmaker)
