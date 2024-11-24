from abc import ABC, abstractmethod

from app.schemas.booking import BookingAccountSchema, BookingAccountCreateSchema


class BookingService(ABC):
    @abstractmethod
    async def create_booking_account(
        self, booking_account_create: BookingAccountCreateSchema
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
