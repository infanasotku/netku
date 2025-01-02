from typing import Annotated
from fastapi import APIRouter, Query

from common.contracts.protocols import CreateService
from app.contracts.services import UserService
from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema


class UserRouter:
    def __init__(self, create_user_service: CreateService[UserService]):
        self._create_user_service = create_user_service

        self.router = APIRouter()

        self.router.add_api_route("/", self.get_users_by_id, methods=["GET"])
        self.router.add_api_route("/{id}", self.get_user_by_id, methods=["GET"])
        self.router.add_api_route("/", self.create_user, methods=["POST"])
        self.router.add_api_route("/{id}", self.update_user, methods=["PATCH"])

    async def get_users_by_id(
        self, ids: Annotated[list[int], Query()]
    ) -> list[UserSchema]:
        async with self._create_user_service() as service:
            return await service.get_users_by_id(ids)

    async def get_user_by_id(self, id: int) -> UserSchema | None:
        async with self._create_user_service() as service:
            return await service.get_user_by_id(id)

    async def create_user(self, user_create: UserCreateSchema) -> UserSchema:
        async with self._create_user_service() as service:
            return await service.create_user(user_create)

    async def update_user(self, user_update: UserUpdateSchema) -> UserSchema:
        async with self._create_user_service() as service:
            return await service.update_user(user_update)
