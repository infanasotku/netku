from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.contracts.repositories import (
    XrayRepository,
    UserRepository,
    BookingRepository,
    AvailabilityRepository,
)
from app.contracts.protocols import CreateClient, CreateRepository, CreateService
from app.contracts.services import UserService, BookingService
from app.contracts.clients import (
    XrayClient,
    BookingClient,
    AssistantClient,
    NotificationClient,
)

from app.services.booking import BookingServiceImpl
from app.services.user import UserServiceImpl
from app.services.xray import XrayServiceImpl
from app.services.availability import AvailabilityServiceImpl
from app.services.analysis.user_booking import BookingAnalysisServiceImpl


class UserServiceFactory:
    def __init__(
        self,
        create_user_repository: CreateRepository[UserRepository],
        create_notification_client: CreateClient[NotificationClient],
    ):
        self._create_user_repository = create_user_repository
        self._create_notification_client = create_notification_client

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[UserServiceImpl, None]:
        async with (
            self._create_notification_client() as notification_client,
            self._create_user_repository() as user_repository,
        ):
            yield UserServiceImpl(user_repository, notification_client)


class BookingServiceFactory:
    def __init__(
        self,
        create_booking_repository: CreateRepository[BookingRepository],
        create_booking_client: CreateClient[BookingClient],
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
        create_xray_repository: CreateRepository[XrayRepository],
        create_xray_client: CreateClient[XrayClient],
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
        create_booking_service: CreateService[BookingService],
        create_user_service: CreateService[UserService],
    ):
        self._create_booking_service = create_booking_service
        self._create_user_service = create_user_service

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[BookingAnalysisServiceImpl, None]:
        async with (
            self._create_booking_service() as booking_service,
            self._create_user_service() as user_service,
        ):
            yield BookingAnalysisServiceImpl(booking_service, user_service)


class AvailabilityServiceFactory:
    def __init__(
        self,
        create_booking_client: CreateClient[BookingClient],
        create_xray_client: CreateClient[XrayClient],
        create_assistant_client: CreateClient[AssistantClient],
        create_availability_repository: CreateRepository[AvailabilityRepository],
        create_user_service: CreateService[UserService],
    ):
        self._create_xray_client = create_xray_client
        self._create_booking_client = create_booking_client
        self._create_assistant_client = create_assistant_client
        self._create_availability_repository = create_availability_repository
        self._create_user_service = create_user_service

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[AvailabilityServiceImpl, None]:
        async with (
            self._create_booking_client() as booking_client,
            self._create_xray_client() as xray_client,
            self._create_assistant_client() as assistant_client,
            self._create_availability_repository() as availability_repository,
            self._create_user_service() as user_service,
        ):
            yield AvailabilityServiceImpl(
                availability_repository,
                booking_client,
                xray_client,
                assistant_client,
                user_service,
            )
