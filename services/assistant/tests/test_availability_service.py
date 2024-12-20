import pytest

from app.schemas.availability import (
    AvailabilityCreateSchema,
    AvailabilitySchema,
    Service,
)
from app.services.availability import AvailabilityServiceImpl

from tests.stubs import (
    StubXrayClient,
    StubAvailabilityRepository,
    StubBookingClient,
    StubAssistantClient,
    StubUserService,
)


class _StubXrayClient(StubXrayClient):
    def __init__(self, status: bool):
        self.status = status

    async def check_health(self):
        return self.status


class _StubAssistantClient(StubAssistantClient):
    def __init__(self, status: bool):
        self.status = status

    async def check_health(self):
        return self.status


class _StubBookingClient(StubBookingClient):
    def __init__(self, status: bool):
        self.status = status

    async def check_health(self):
        return self.status


class _StubAvailabilityRepository(StubAvailabilityRepository):
    def __init__(self):
        self.logged = False

    async def log_availability(self, _: AvailabilityCreateSchema) -> AvailabilitySchema:
        self.logged = True


class _StubUserService(StubUserService):
    def __init__(self):
        self.sended = False

    async def send_notify_by_subscriptions(
        self, subscriptions: list[str], message: str
    ) -> None:
        self.sended = True


@pytest.mark.parametrize(
    "service",
    [Service.assistant, Service.xray, Service.booking],
)
@pytest.mark.asyncio
async def test_checking_positiv_availability(service: Service):
    stub_xray_client = _StubXrayClient(True)
    stub_booking_client = _StubBookingClient(True)
    stub_assistant_client = _StubAssistantClient(True)
    stub_repository = _StubAvailabilityRepository()
    stub_user_service = _StubUserService()

    availability_service = AvailabilityServiceImpl(
        stub_repository,
        stub_booking_client,
        stub_xray_client,
        stub_assistant_client,
        stub_user_service,
    )

    await availability_service.check_availability(service)

    assert stub_repository.logged
    assert not stub_user_service.sended


@pytest.mark.parametrize(
    "service",
    [Service.assistant, Service.xray, Service.booking],
)
@pytest.mark.asyncio
async def test_checking_negativ_availability(service: Service):
    stub_xray_client = _StubXrayClient(False)
    stub_booking_client = _StubBookingClient(False)
    stub_assistant_client = _StubAssistantClient(False)
    stub_repository = _StubAvailabilityRepository()
    stub_user_service = _StubUserService()

    availability_service = AvailabilityServiceImpl(
        stub_repository,
        stub_booking_client,
        stub_xray_client,
        stub_assistant_client,
        stub_user_service,
    )

    await availability_service.check_availability(service)

    assert stub_repository.logged
    assert stub_user_service.sended
