from datetime import datetime, timedelta
from fastapi.testclient import TestClient
import pytest

from app import app
from app.container import Container
from app.adapters.input.api.router import router

from common.contracts.services import AuthService
from common.schemas.token import TokenPayload
from app.contracts.services import UserService
from app.schemas.user import UserSchema


class UserServiceStub(UserService):
    async def get_users_by_id(self, ids):
        return [UserSchema(id=ids[0], phone_number=None, telegram_id=None)]

    async def get_user_by_telegram_id(self, id):
        raise NotImplementedError

    async def get_user_by_phone(self, phone):
        raise NotImplementedError

    async def get_users(self):
        raise NotImplementedError

    async def create_user(self, user_create):
        return UserSchema(
            id=user_create.id,
            phone_number=user_create.phone_number,
            telegram_id=user_create.telegram_id,
        )

    async def update_user(self, user_id, user_update):
        raise NotImplementedError


class AuthServiceStub(AuthService):
    async def introspect(self, token):
        return TokenPayload(
            client_id="test",
            scopes=["admin"],
            expire=datetime.now() + timedelta(days=1),
        )


client = TestClient(router)
auth_service = AuthServiceStub()
user_service = UserServiceStub()
container: Container = app.container


@pytest.mark.parametrize(
    "id",
    [1, 2, 3],
)
def test_get_user_by_id(id):
    with (
        container.user_service.override(user_service),
        container.auth_container.container.auth_service.override(auth_service),
    ):
        response = client.get(f"/{id}", headers={"Authorization": "Bearer test"})

    assert response.status_code == 200
    assert response.json()["id"] == id


@pytest.mark.parametrize(
    "id",
    [1, 2, 3],
)
def test_create_user(id):
    with (
        container.user_service.override(user_service),
        container.auth_container.container.auth_service.override(auth_service),
    ):
        response = client.post(
            "/",
            json={"id": id, "telegram_id": None, "phone_number": None},
            headers={"Authorization": "Bearer test"},
        )

    assert response.status_code == 200
    assert response.json()["id"] == id
