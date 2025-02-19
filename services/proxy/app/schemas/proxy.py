from pydantic import Field
from datetime import datetime
from uuid import UUID


from common import now
from common.schemas import BaseSchema


class ProxyInfoCreateSchema(BaseSchema):
    uuid: UUID
    last_update: datetime = Field(
        default_factory=now,
    )
    synced_with_xray: bool = Field(default=False)


class ProxyInfoUpdateSchema(ProxyInfoCreateSchema):
    pass


class ProxyInfoSchema(ProxyInfoCreateSchema):
    pass
