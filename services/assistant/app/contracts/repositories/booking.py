from abc import abstractmethod

from app.schemas.booking import BookingAccountSchema, BookingAccountCreateSchema

from app.contracts.repositories.base import BaseRepository


class BookingRepository(BaseRepository):
    @abstractmethod
    async def get_booking_account_by_id(self, id: int) -> BookingAccountSchema | None:
        """Gets booking account by `id`.

        :return: booking account if it exist in DB, `None` otherwise."""

    @abstractmethod
    async def create_booking_account(
        self, account_create: BookingAccountCreateSchema
    ) -> BookingAccountSchema:
        """Creates booking account in DB.

        :return: Created booking account.
        """
