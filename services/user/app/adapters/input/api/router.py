from typing import Annotated
from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import Provide, inject

from app.container import Container
from app.contracts.services import UserService
from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema


router = APIRouter()


@router.get("/")
@inject
async def get_users_by_id(
    ids: Annotated[list[int], Query()],
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> list[UserSchema]:
    return await user_service.get_users_by_id(ids)


@router.get("/{id}")
@inject
async def get_user_by_id(
    id: int, user_service: UserService = Depends(Provide[Container.user_service])
) -> UserSchema | None:
    return await user_service.get_user_by_id(id)


@router.post("/")
@inject
async def create_user(
    user_create: UserCreateSchema,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> UserSchema:
    return await user_service.create_user(user_create)


@router.patch("/{id}")
@inject
async def update_user(
    user_update: UserUpdateSchema,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> UserSchema:
    return await user_service.update_user(user_update)
