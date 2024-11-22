from sqlalchemy import select

from app.repositories.xray_repository import XrayRepository

from app.database.repositories.base_repository import BaseRepository
from app.schemas.xray_schemas import (
    XrayRecordSchema,
    XrayRecordCreateSchema,
    XrayRecordUpdateSchema,
)

from app.database import converters
from app.database.models import XrayRecord
from app.database.orm import selectinload_all


class SQLXrayRepository(XrayRepository, BaseRepository):
    async def _get_xray_record_model_by_id(self, id: int) -> XrayRecord | None:
        s = (
            select(XrayRecord)
            .options(*selectinload_all(XrayRecord))
            .filter(XrayRecord.id == id)
        )
        return (await self.session.execute(s)).scalars().first()

    async def get_xray_record_by_id(self, id: int) -> XrayRecordSchema | None:
        xray_record = await self._get_xray_record_model_by_id(id)

        if xray_record is None:
            return None

        return converters.xray_record_to_xray_record_schema(xray_record)

    async def create_xray_record(
        self, xray_record_create: XrayRecordCreateSchema
    ) -> XrayRecordSchema:
        xray_record = converters.xray_record_create_schema_to_xray_record(
            xray_record_create
        )
        self.session.add(xray_record)
        await self.session.flush()
        await self.session.refresh(xray_record)

        return converters.xray_record_to_xray_record_schema(xray_record)

    async def update_xray_record(
        self, xray_record_id: int, xray_record_update: XrayRecordUpdateSchema
    ) -> XrayRecordSchema:
        xray_record = await self._get_xray_record_model_by_id(xray_record_id)

        if xray_record is None:
            raise Exception(f"Xray record with id {xray_record_id} not exist.")

        for field, value in xray_record_update.model_dump(exclude_unset=True).items():
            setattr(xray_record, field, value)

        await self.session.flush()
        await self.session.refresh(xray_record)

        return converters.xray_record_to_xray_record_schema(xray_record)
