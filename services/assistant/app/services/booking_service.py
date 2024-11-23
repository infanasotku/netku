from abc import ABC, abstractmethod

from app.repositories import BookingRepository
from app.schemas.booking_schemas import BookingAccountSchema, BookingAccountCreateSchema
from app.clients.booking_client import BookingClient


class AbstractBookingService(ABC):
    @abstractmethod
    async def create_booking_account(
        self, user_id: int, email: str, password: str
    ) -> BookingAccountSchema | None:
        """:return: booking account if it created, `None` otherwise."""

    @abstractmethod
    async def get_booking_account_by_id(self, id: int) -> BookingAccountSchema | None:
        """:return: Booking account by `id`."""

    @abstractmethod
    async def booked(self, email: str, password: str) -> bool:
        """:return: `True` if mashine booked, `False` otherwise."""

    @abstractmethod
    async def run_booking(self, email: str, password: str) -> bool:
        """Runs booking for given `email` and `password`.

        :return: `True` if booking ran, `False` otherwise."""

    @abstractmethod
    async def stop_booking(self, email: str, password: str) -> None:
        """Stops booking for given `email` and `password`."""


class BookingService(AbstractBookingService):
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
