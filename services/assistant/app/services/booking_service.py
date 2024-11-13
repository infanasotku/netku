from abc import ABC, abstractmethod


from app.database.models import BookingAccount, User
from app.database.orm import AbstractRepository

from app.schemas.booking_schemas import BookingAccountSchema

from app.infra.grpc import AbstractBookingClient


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
        repository: AbstractRepository,
        booking_client: AbstractBookingClient,
    ):
        self.repository = repository
        self.booking_client = booking_client

    async def create_booking_account(
        self, user_id: int, email: str, password: str
    ) -> BookingAccountSchema | None:
        raw_user = await self.repository.find_first(User, User.id, user_id)

        if raw_user is None:
            return None

        booking_account = BookingAccount(email=email, password=password, owner=raw_user)

        return await self.repository.create(booking_account)

    async def get_booking_account_by_id(self, id: int) -> BookingAccountSchema | None:
        account = await self.repository.find_first(
            BookingAccount, BookingAccount.id, id
        )
        return (
            BookingAccountSchema.model_validate(account)
            if account is not None
            else None
        )

    async def booked(self, email: str, password: str) -> bool:
        return await self.booking_client.booked(email, password)

    async def run_booking(self, email: str, password: str) -> bool:
        return await self.booking_client.run_booking(email, password)

    async def stop_booking(self, email: str, password: str) -> None:
        await self.booking_client.stop_booking(email, password)
