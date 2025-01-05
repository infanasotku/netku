from common.schemas import BaseSchema, BaseSchemaPK


class ClientUpdateSchema(BaseSchema):
    client_id: str | None = None
    hashed_client_secret: str | None = None


class ClientCreateSchema(BaseSchemaPK):
    client_id: str
    hashed_client_secret: str


class ClientSchema(ClientCreateSchema):
    scopes: list[str]


class TokenPayload(BaseSchema):
    client_id: str
    scopes: list[str]
