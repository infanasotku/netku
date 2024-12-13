from datetime import datetime
from typing import Awaitable, Callable

from app.contracts.repositories import AvailabilityRepository
from app.contracts.services import AvailabilityService, UserService
from app.contracts.clients import (
    BookingClient,
    XrayClient,
    AssistantClient,
    TelegramClient,
)

from app.schemas.availability import (
    AvailabilitySchema,
    Service,
    AvailabilityCreateSchema,
)


class AvailabilityServiceImpl(AvailabilityService):
    def __init__(
        self,
        availability_repository: AvailabilityRepository,
        booking_client: BookingClient,
        xray_client: XrayClient,
        assistant_client: AssistantClient,
        telegram_client: TelegramClient,
        user_service: UserService,
    ):
        self._availability_repository = availability_repository
        self._booking_client = booking_client
        self._xray_client = xray_client
        self._assistant_client = assistant_client
        self._telegram_client = telegram_client
        self._user_service = user_service

    async def check_availability(
        self,
        service: Service,
        retries_count: int = 10,
        notify_factor_level: float = 0.5,
    ) -> AvailabilitySchema:
        average_response_time = None
        availability_count = 0

        check_health: Callable[[], Awaitable[bool]]

        match service:
            case Service.xray:
                check_health = self._xray_client.check_health
            case Service.booking:
                check_health = self._booking_client.check_health
            case Service.assistant:
                check_health = self._assistant_client.check_health
            case _:
                raise Exception(f"Undefined service: {service.name}.")

        for _ in range(retries_count):
            start = datetime.now()
            healthy = await check_health()
            end = datetime.now()

            if healthy:
                availability_count += 1
                average_response_time += (end - start).microseconds * 1000

        availability_factor = availability_count / retries_count
        if availability_count != 0:
            average_response_time /= availability_count

        availability_create = AvailabilityCreateSchema(
            created=datetime.now(),
            service=service,
            availability_factor=availability_factor,
            response_time=average_response_time,
        )

        # await self._availability_repository.log_availability(availability_create)

        if availability_factor <= notify_factor_level:
            users = await self._user_service.get_users_by_active_subscriptions(
                ["availability_subscription"], True
            )

            for user in users:
                if user.telegram_id is None:
                    pass  # TODO: logging
                    continue
                await self._telegram_client.send_message(
                    f"Service not available: {service.name}", user.telegram_id
                )
