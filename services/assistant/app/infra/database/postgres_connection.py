from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class PostgreSQLConnection:
    def __init__(self, psql_dsn: str):
        self._async_engine = create_async_engine(psql_dsn)
        self._async_session = async_sessionmaker(self._async_engine)

    @asynccontextmanager
    async def get_db(self):
        async with self._async_session.begin() as session:
            yield session
