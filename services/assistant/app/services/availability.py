from app.contracts.repositories import AvailabilityRepository
from app.contracts.services import AvailabilityService
from app.schemas.availability import AvailabilitySchema, Service
from app.contracts.clients import BookingClient, XrayClient, AssistantClient


class AvailabilityServiceImpl(AvailabilityService):
    def __init__(
        self,
        availability_repository: AvailabilityRepository,
        booking_client: BookingClient,
        xray_client: XrayClient,
        assistant_client: AssistantClient,
    ):
        self._availability_repository = availability_repository
        self._booking_client = booking_client
        self._xray_client = xray_client
        self._assistant_client = assistant_client

    async def check_availability(self, service: Service) -> AvailabilitySchema:
        raise NotImplementedError
