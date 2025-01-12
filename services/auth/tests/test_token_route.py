from datetime import datetime, timedelta
from fastapi.testclient import TestClient
import pytest

from app import app
from app.container import Container
from app.adapters.input.api.auth.token import router

from common.schemas.token import TokenPayload
from app.contracts.services import ClientService
from app.schemas.token import TokenSchema


class ClientServiceStub(ClientService):
    async def introspect(self, token):
        return TokenPayload(
            client_id=token,
            scopes=["admin"],
            expire=datetime.now() + timedelta(days=1),
        )

    async def get_client_with_scopes_by_client_id(self, client_id):
        raise NotImplementedError

    async def authenticate(self, client_id, client_secret):
        return TokenSchema(access_token=client_id, token_type="Bearer")


client = TestClient(router)
client_service = ClientServiceStub()
container: Container = app.container


@pytest.mark.parametrize(
    "client_id",
    ["test1", "test2", "test3"],
)
def test_introspect_token(client_id: str):
    with (
        container.client_service.override(client_service),
    ):
        response = client.post(
            "/introspect",
            json=client_id,
            headers={"Authorization": "Bearer test"},
        )

    assert response.status_code == 200
    assert response.json()["client_id"] == client_id


@pytest.mark.parametrize(
    "client_id",
    ["test1", "test2", "test3"],
)
def test_create_token(client_id: str):
    with (
        container.client_service.override(client_service),
    ):
        response = client.post(
            "/",
            json={"client_id": client_id, "client_secret": "test"},
            headers={"Authorization": "Bearer test"},
        )

    assert response.status_code == 200
    assert response.json()["access_token"] == client_id
