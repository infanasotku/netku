from sqlalchemy.ext.asyncio import AsyncSession


class SQLBaseRepository:
    def __init__(self, session: AsyncSession):
        self._session = session