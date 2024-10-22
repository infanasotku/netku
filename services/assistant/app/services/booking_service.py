from typing import Optional


from app.database.models import BookingAccount
from app.database.orm import AbstractRepository
from app.database.schemas import BookingAccountSchema, UserSchema

from app.infra.grpc import AbstractBookingClient


class BookingService:
    def __init__(
        self, repository: AbstractRepository, booking_client: AbstractBookingClient
    ):
        self.repository = repository
        self.booking_client = booking_client

    async def create_booking_account(
        self, user: UserSchema, email: str, password: str
    ) -> bool:
        return await self.repository.create_booking_account(user, email, password)

    async def get_booking_account_by_id(
        self, id: int
    ) -> Optional[BookingAccountSchema]:
        """:return: Booking account by `id`."""
        account = await self.repository.find_first(
            BookingAccount, BookingAccount.id, id
        )
        return (
            BookingAccountSchema.model_validate(account)
            if account is not None
            else None
        )

    async def booked(self, email: str, password: str) -> bool:
        """:return: `True` if mashine booked, `False` otherwise."""
        return await self.booking_client.booked(email, password)

    async def run_booking(self, email: str, password: str) -> None:
        """Runs booking for given `email` and `password`."""
        await self.booking_client.run_booking(email, password)

    async def stop_booking(self, email: str, password: str) -> None:
        """Stops booking for given `email` and `password`."""
        await self.booking_client.stop_booking(email, password)
