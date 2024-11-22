from datetime import datetime
from uuid import UUID
from app.schemas.base_schema import BaseSchema, BaseSchemaPK


class XrayRecordCreateSchema(BaseSchemaPK):
    uid: UUID
    last_update: datetime


class XrayRecordUpdateSchema(BaseSchema):
    uid: UUID | None = None
    last_update: datetime | None = None


class XrayRecordSchema(XrayRecordCreateSchema):
    pass
