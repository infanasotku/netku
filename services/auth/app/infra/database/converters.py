from app.infra.database.models import Client
from app.schemas.client import ClientSchema


def client_to_client_schema(client: Client) -> ClientSchema:
    return ClientSchema.model_validate(client)
