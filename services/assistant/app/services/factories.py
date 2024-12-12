from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncGenerator, Callable

from app.contracts.repositories import (
    XrayRepository,
    UserRepository,
    BookingRepository,
    AvailabilityRepository,
)
from app.contracts.services import UserService, BookingService
from app.contracts.clients import (
    XrayClient,
    BookingClient,
    AssistantClient,
    TelegramClient,
)

from app.services.booking import BookingServiceImpl
from app.services.user import UserServiceImpl
from app.services.xray import XrayServiceImpl
from app.services.availability import AvailabilityServiceImpl
from app.services.analysis.user_booking import BookingAnalysisServiceImpl


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


class BookingAnalysisServiceFactory:
    def __init__(
        self,
        create_booking_service: Callable[[], AsyncContextManager[BookingService]],
        create_user_service: Callable[[], AsyncContextManager[UserService]],
    ):
        self._create_booking_service = create_booking_service
        self._create_user_service = create_user_service

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[XrayServiceImpl, None]:
        async with (
            self._create_booking_service() as booking_service,
            self._create_user_service() as user_service,
        ):
            yield BookingAnalysisServiceImpl(booking_service, user_service)


class AvailabilityServiceFactory:
    def __init__(
        self,
        create_booking_client: Callable[[], AsyncContextManager[BookingClient]],
        create_xray_client: Callable[[], AsyncContextManager[XrayClient]],
        create_assistant_client: Callable[[], AsyncContextManager[AssistantClient]],
        create_telegram_client: Callable[[], AsyncContextManager[TelegramClient]],
        create_availability_repository: Callable[
            [], AsyncContextManager[AvailabilityRepository]
        ],
    ):
        self._create_xray_client = create_xray_client
        self._create_booking_client = create_booking_client
        self._create_assistant_client = create_assistant_client
        self._create_telegram_client = create_telegram_client
        self._create_availability_repository = create_availability_repository

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[XrayServiceImpl, None]:
        async with (
            self._create_booking_client() as booking_client,
            self._create_xray_client() as xray_client,
            self._create_assistant_client() as assistant_client,
            self._create_availability_repository() as availability_repository,
            self._create_telegram_client() as telegram_client,
        ):
            yield AvailabilityServiceImpl(
                availability_repository,
                booking_client,
                xray_client,
                assistant_client,
                telegram_client,
            )
