from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm import Repository

from infra.grpc.booking_client import BookingClient

from services.booking_service import BookingService
from services.user_service import UserService


class UserServiceFactory:
    def __init__(self, get_db: Callable[[], AsyncContextManager[AsyncSession]]):
        self.get_db = get_db

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[UserService, None]:
        async with self.get_db() as session:
            yield UserService(Repository(session))


class BookingServiceFactory:
    def __init__(
        self,
        get_db: Callable[[], AsyncContextManager[AsyncSession]],
        create_booking_client: Callable[[], AsyncContextManager[BookingClient]],
    ):
        self.get_db = get_db
        self.create_booking_client = create_booking_client

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[BookingService, None]:
        async with (
            self.get_db() as session,
            self.create_booking_client() as booking_client,
        ):
            yield BookingService(Repository(session), booking_client)
