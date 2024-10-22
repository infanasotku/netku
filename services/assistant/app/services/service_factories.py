from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm import Repository

from app.infra.grpc import BookingClient, XrayClient

from app.services.booking_service import BookingService
from app.services.user_service import UserService
from app.services.xray_service import XrayService


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


class XrayServiceFactory:
    def __init__(
        self,
        get_db: Callable[[], AsyncContextManager[AsyncSession]],
        create_xray_client: Callable[[], AsyncContextManager[XrayClient]],
    ):
        self.get_db = get_db
        self.create_xray_client = create_xray_client

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[XrayService, None]:
        async with (
            self.get_db() as session,
            self.create_xray_client() as xray_client,
        ):
            yield XrayService(Repository(session), xray_client)
