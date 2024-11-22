from abc import ABC, abstractmethod

from app.schemas.xray_schemas import (
    XrayRecordSchema,
    XrayRecordCreateSchema,
    XrayRecordUpdateSchema,
)


class BookingRepository(ABC):
    @abstractmethod
    async def get_xray_record_by_id(self, id: int) -> XrayRecordSchema | None:
        """Gets xray record by `id`.

        :return: xray record if it exist in DB, `None` otherwise."""

    @abstractmethod
    async def create_xray_record(
        self, account_create: XrayRecordCreateSchema
    ) -> XrayRecordSchema:
        """Creates xray record in DB.

        :return: Created xray record.
        """

    @abstractmethod
    async def update_xray_record(
        self, user_id: int, user_update: XrayRecordUpdateSchema
    ) -> XrayRecordSchema:
        """Update xray record in DB.

        :return: Updated xray record.
        """
