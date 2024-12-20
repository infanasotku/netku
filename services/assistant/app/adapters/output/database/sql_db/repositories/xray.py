from sqlalchemy import select

from app.contracts.repositories import XrayRepository

from app.adapters.output.database.sql_db.repositories.base import SQLBaseRepository
from app.schemas.xray import (
    XrayRecordSchema,
    XrayRecordCreateSchema,
    XrayRecordUpdateSchema,
)

from app.adapters.output.database.sql_db import converters
from app.adapters.output.database.sql_db.models import XrayRecord
from app.adapters.output.database.sql_db.orm import selectinload_all


class SQLXrayRepository(XrayRepository, SQLBaseRepository):
    async def _get_xray_record_model_by_id(self, id: int) -> XrayRecord | None:
        s = (
            select(XrayRecord)
            .options(*selectinload_all(XrayRecord))
            .filter(XrayRecord.id == id)
        )
        return (await self._session.execute(s)).scalars().first()

    async def get_last_xray_record(self) -> XrayRecordSchema | None:
        s = (
            select(XrayRecord)
            .options(*selectinload_all(XrayRecord))
            .order_by(XrayRecord.id.desc())
            .limit(1)
        )
        xray_record = (await self._session.execute(s)).scalars().first()

        if xray_record is None:
            return None

        return converters.xray_record_to_xray_record_schema(xray_record)

    async def create_xray_record(
        self, xray_record_create: XrayRecordCreateSchema
    ) -> XrayRecordSchema:
        xray_record = converters.xray_record_create_schema_to_xray_record(
            xray_record_create
        )
        self._session.add(xray_record)
        await self._session.flush()
        await self._session.refresh(xray_record)

        return converters.xray_record_to_xray_record_schema(xray_record)

    async def update_xray_record(
        self, xray_record_id: int, xray_record_update: XrayRecordUpdateSchema
    ) -> XrayRecordSchema:
        xray_record = await self._get_xray_record_model_by_id(xray_record_id)

        if xray_record is None:
            raise Exception(f"Xray record with id {xray_record_id} not exist.")

        for field, value in xray_record_update.model_dump(exclude_unset=True).items():
            setattr(xray_record, field, value)

        await self._session.flush()
        await self._session.refresh(xray_record)

        return converters.xray_record_to_xray_record_schema(xray_record)
