from datetime import datetime
from uuid import UUID
from pydantic import Field

from common.schemas import BaseSchema
from common.schemas.proxy import ProxyInfoSchema


class ProxyInfoCreateSchema(BaseSchema):
    running: bool = Field(default=False)
    created: datetime
    uuid: UUID | None = None
    addr: str
    key: str


class ProxyInfoUpdateSchema(BaseSchema):
    running: bool | None = None
    uuid: UUID | None = None


class ProxyInfoFullSchema(ProxyInfoSchema):
    event_id: UUID
