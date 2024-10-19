from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm import Repository

from services.booking_service import BookingService
from services.user_service import UserService


class UserServiceFactory:
    def __init__(self, get_db: Callable[[], AsyncContextManager[AsyncSession]]):
        self.get_db = get_db

    @asynccontextmanager
    async def create_user_service(self) -> AsyncGenerator[UserService, None]:
        async with self.get_db() as session:
            yield UserService(Repository(session))


class BookingServiceFactory:
    def __init__(self, get_db: Callable[[], AsyncContextManager[AsyncSession]]):
        self.get_db = get_db

    @asynccontextmanager
    async def create_booking_service(self) -> AsyncGenerator[BookingService, None]:
        async with self.get_db() as session:
            yield BookingService(Repository(session))
