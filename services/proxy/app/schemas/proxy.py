from pydantic import Field
from datetime import datetime
from uuid import UUID


from common import now
from common.schemas import BaseSchema


class ProxyInfoBaseSchema(BaseSchema):
    last_update: datetime = Field(
        default_factory=now,
    )
    synced_with_xray: bool = Field(default=False)


class ProxyInfoCreateSchema(ProxyInfoBaseSchema):
    uuid: UUID


class ProxyInfoUpdateSchema(ProxyInfoBaseSchema):
    uuid: UUID | None = None


class ProxyInfoSchema(ProxyInfoCreateSchema):
    pass
