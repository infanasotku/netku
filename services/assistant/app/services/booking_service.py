from typing import Optional

from database.models import BookingAccount
from database.orm import AbstractRepository
from database.schemas import BookingAccountSchema, UserSchema


class BookingService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

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
