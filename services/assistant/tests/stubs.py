from app.contracts.repositories import XrayRepository
from app.schemas.xray import (
    XrayRecordCreateSchema,
    XrayRecordSchema,
    XrayRecordUpdateSchema,
)


class StubXrayRepository(XrayRepository):
    async def get_last_xray_record(self) -> XrayRecordSchema | None:
        raise NotImplementedError

    async def create_xray_record(
        self, account_create: XrayRecordCreateSchema
    ) -> XrayRecordSchema:
        raise NotImplementedError

    async def update_xray_record(
        self, user_id: int, user_update: XrayRecordUpdateSchema
    ) -> XrayRecordSchema:
        raise NotImplementedError
