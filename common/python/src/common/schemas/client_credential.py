from common.schemas import BaseSchema


class ClientCredentials(BaseSchema):
    client_id: str
    scopes: list[str]
