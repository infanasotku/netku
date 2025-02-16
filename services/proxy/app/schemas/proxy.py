from datetime import datetime
from uuid import UUID


from common.schemas import BaseSchema


class ProxyInfoCreateSchema(BaseSchema):
    uuid: UUID
    last_update: datetime


class ProxyInfoUpdateSchema(BaseSchema):
    uuid: UUID | None = None
    last_update: datetime | None = None


class ProxyInfoSchema(ProxyInfoCreateSchema):
    pass
