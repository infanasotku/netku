from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    Query,
    Security,
)
from dependency_injector.wiring import Provide, inject
from contextlib import AbstractAsyncContextManager

from app.container import Container
from common.schemas.client_credential import ClientCredentials
from app.contracts.services import UserService
from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema

from app.adapters.input.api.dependencies import Authorization

router = APIRouter()


@router.get("/")
@inject
async def get_users_by_id(
    ids: Annotated[list[int], Query()],
    user_service_context: AbstractAsyncContextManager[UserService] = Depends(
        Provide[Container.user_service]
    ),
    _: ClientCredentials = Security(
        Authorization,
        scopes=["users:read"],
    ),
) -> list[UserSchema]:
    async with user_service_context as user_service:
        return await user_service.get_users_by_id(ids)


@router.get("/{id}")
@inject
async def get_user_by_id(
    id: int,
    user_service_context: AbstractAsyncContextManager[UserService] = Depends(
        Provide[Container.user_service]
    ),
    _: ClientCredentials = Security(
        Authorization,
        scopes=["users:read"],
    ),
) -> UserSchema | None:
    async with user_service_context as user_service:
        return await user_service.get_user_by_id(id)


@router.post("/")
@inject
async def create_user(
    user_create: UserCreateSchema,
    user_service_context: AbstractAsyncContextManager[UserService] = Depends(
        Provide[Container.user_service]
    ),
    _: ClientCredentials = Security(
        Authorization,
        scopes=["users:write"],
    ),
) -> UserSchema:
    async with user_service_context as user_service:
        return await user_service.create_user(user_create)


@router.patch("/{id}")
@inject
async def update_user(
    id: int,
    user_update: UserUpdateSchema,
    user_service_context: AbstractAsyncContextManager[UserService] = Depends(
        Provide[Container.user_service]
    ),
    _: ClientCredentials = Security(
        Authorization,
        scopes=["users:write"],
    ),
) -> UserSchema:
    async with user_service_context as user_service:
        return await user_service.update_user(id, user_update)
