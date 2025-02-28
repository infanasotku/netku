import datetime
from uuid import UUID
from pydantic import Field
from common.schemas import BaseSchema


class ProxyInfoCreateSchema(BaseSchema):
    running: bool = Field(default=False)
    created: datetime
    uuid: UUID
    addr: str
    key: str


class ProxyInfoUpdateSchema(BaseSchema):
    running: bool | None = None
    uuid: UUID | None = None
