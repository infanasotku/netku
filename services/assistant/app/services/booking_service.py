from app.contracts.repositories import BookingRepository
from app.contracts.services import BookingService
from app.schemas.booking_schemas import BookingAccountSchema, BookingAccountCreateSchema
from app.contracts.clients.booking_client import BookingClient


class BookingServiceImpl(BookingService):
    def __init__(
        self,
        booking_repository: BookingRepository,
        booking_client: BookingClient,
    ):
        self._booking_repository = booking_repository
        self._booking_client = booking_client

    async def create_booking_account(
        self, booking_account_create: BookingAccountCreateSchema
    ) -> BookingAccountSchema | None:
        return await self._booking_repository.create_booking_account(
            booking_account_create
        )

    async def get_booking_account_by_id(self, id: int) -> BookingAccountSchema | None:
        return await self._booking_repository.get_booking_account_by_id(id)

    async def booked(self, email: str, password: str) -> bool:
        return await self._booking_client.booked(email, password)

    async def run_booking(self, email: str, password: str) -> bool:
        return await self._booking_client.run_booking(email, password)

    async def stop_booking(self, email: str, password: str) -> None:
        await self._booking_client.stop_booking(email, password)
