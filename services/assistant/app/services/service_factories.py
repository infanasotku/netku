from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncGenerator, Callable

from app.contracts.repositories import XrayRepository, UserRepository, BookingRepository

from app.contracts.clients.xray_client import XrayClient
from app.contracts.clients.booking_client import BookingClient

from app.services.booking_service import BookingServiceImpl
from app.services.user_service import UserServiceImpl
from app.services.xray_service import XrayServiceImpl


class UserServiceFactory:
    def __init__(
        self,
        create_user_repository: Callable[[], AsyncContextManager[UserRepository]],
    ):
        self._create_user_repository = create_user_repository

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[UserServiceImpl, None]:
        async with self._create_user_repository() as user_repository:
            yield UserServiceImpl(user_repository)


class BookingServiceFactory:
    def __init__(
        self,
        create_booking_repository: Callable[[], AsyncContextManager[BookingRepository]],
        create_booking_client: Callable[[], AsyncContextManager[BookingClient]],
    ):
        self._create_booking_repository = create_booking_repository
        self._create_booking_client = create_booking_client

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[BookingServiceImpl, None]:
        async with (
            self._create_booking_repository() as booking_repository,
            self._create_booking_client() as booking_client,
        ):
            yield BookingServiceImpl(booking_repository, booking_client)


class XrayServiceFactory:
    def __init__(
        self,
        create_xray_repository: Callable[[], AsyncContextManager[XrayRepository]],
        create_xray_client: Callable[[], AsyncContextManager[XrayClient]],
    ):
        self._create_xray_repository = create_xray_repository
        self._create_xray_client = create_xray_client

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[XrayServiceImpl, None]:
        async with (
            self._create_xray_repository() as xray_repository,
            self._create_xray_client() as xray_client,
        ):
            yield XrayServiceImpl(xray_repository, xray_client)
