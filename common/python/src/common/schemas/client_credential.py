from common.schemas.base import BaseSchema


class ClientCredentials(BaseSchema):
    client_id: str
    scopes: list[str]
