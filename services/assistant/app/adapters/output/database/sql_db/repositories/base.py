from sqlalchemy.ext.asyncio import AsyncSession

from app.contracts.repositories.base import BaseRepository


class SQLBaseRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
