from contextlib import asynccontextmanager
from fastapi.testclient import TestClient
import pytest

from app.contracts.services import UserService
from app.schemas.user import UserSchema

from app.adapters.input.api import create_api


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


@asynccontextmanager
async def create_user_service_stub():
    yield UserServiceStub()


api = create_api(create_user_service_stub)
client = TestClient(api)


@pytest.mark.parametrize(
    "id",
    [1, 2, 3],
)
def test_get_user_by_id(id):
    response = client.get(f"/api/users/{id}")

    assert response.status_code == 200
    assert response.json()["id"] == id


@pytest.mark.parametrize(
    "id",
    [1, 2, 3],
)
def test_create_user(id):
    response = client.post(
        "/api/users/", json={"id": id, "telegram_id": None, "phone_number": None}
    )

    assert response.status_code == 200
    assert response.json()["id"] == id
