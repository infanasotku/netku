from common.schemas.base import BaseSchema


class ClientCredentials(BaseSchema):
    external_client_id: str
    scopes: list[str]
