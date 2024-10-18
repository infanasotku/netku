from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable

from database.orm import Repository

from services.booking_service import BookingService
from services.user_service import UserService


class ServiceFactory:
    """Specifies factory for DB services."""

    def __init__(self, get_db: Callable):
        self.get_db = get_db

    @asynccontextmanager
    async def user_service_factory(self) -> AsyncGenerator[UserService, None]:
        async with self.get_db() as session:
            yield UserService(Repository(session))

    @asynccontextmanager
    async def booking_service_factory(self) -> AsyncGenerator[BookingService, None]:
        async with self.get_db() as session:
            yield BookingService(Repository(session))
