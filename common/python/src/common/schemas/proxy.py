from uuid import UUID

from common.schemas import BaseSchema


class ProxyInfo(BaseSchema):
    uuid: UUID
