from contextlib import asynccontextmanager
from dependency_injector import providers
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
            external_client_id=token,
            scopes=["admin"],
            expire=datetime.now() + timedelta(days=1),
        )

    async def get_client_with_scopes_by_external_client_id(self, external_client_id):
        raise NotImplementedError

    async def authenticate(self, external_client_id, client_secret):
        return TokenSchema(access_token=external_client_id, token_type="Bearer")

    async def remove_client_scope(self, client_scope_id):
        raise NotImplementedError

    async def create_client_scope(self, external_client_id, scope_id):
        raise NotImplementedError


client = TestClient(router)
client_service = ClientServiceStub()
container: Container = app.container


@asynccontextmanager
async def get_client_service():
    yield client_service


@pytest.mark.parametrize(
    "external_client_id",
    ["test1", "test2", "test3"],
)
def test_introspect_token(external_client_id: str):
    with (
        container.client_service.override(providers.Factory(get_client_service)),
    ):
        response = client.post(
            "/introspect",
            json=external_client_id,
            headers={"Authorization": "Bearer test"},
        )

    assert response.status_code == 200
    assert response.json()["external_client_id"] == external_client_id


@pytest.mark.parametrize(
    "external_client_id",
    ["test1", "test2", "test3"],
)
def test_create_token(external_client_id: str):
    with (
        container.client_service.override(providers.Factory(get_client_service)),
    ):
        response = client.post(
            "/",
            json={"external_client_id": external_client_id, "client_secret": "test"},
            headers={"Authorization": "Bearer test"},
        )

    assert response.status_code == 200
    assert response.json()["access_token"] == external_client_id
