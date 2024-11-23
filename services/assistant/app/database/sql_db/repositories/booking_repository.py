from sqlalchemy import select

from app.contracts.repositories import BookingRepository

from app.database.sql_db.repositories.base_repository import SQLBaseRepository
from app.schemas.booking_schemas import BookingAccountCreateSchema, BookingAccountSchema

from app.database.sql_db import converters
from app.database.sql_db.models import BookingAccount
from app.database.sql_db.orm import selectinload_all


class SQLBookingRepository(BookingRepository, SQLBaseRepository):
    async def get_booking_account_by_id(self, id: int) -> BookingAccountSchema | None:
        s = (
            select(BookingAccount)
            .options(*selectinload_all(BookingAccount))
            .filter(BookingAccount.id == id)
        )
        account = (await self.session.execute(s)).scalars().first()

        if account is None:
            return None

        return converters.booking_account_to_booking_account_schema(account)

    async def create_booking_account(
        self, account_create: BookingAccountCreateSchema
    ) -> BookingAccountSchema:
        account = converters.booking_account_create_schema_to_booking_account(
            account_create
        )
        self.session.add(account)
        await self.session.flush()
        await self.session.refresh(account)

        return converters.booking_account_to_booking_account_schema(account)
