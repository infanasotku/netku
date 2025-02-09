from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    Query,
    Security,
)
from dependency_injector.wiring import Provide, inject

from app.container import Container
from common.schemas.client_credential import ClientCredentials
from app.contracts.services import UserService
from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema

from app.adapters.input.api.dependencies import Authorization
from app.infra.config.scopes import Scopes

router = APIRouter()


@router.get("/")
@inject
async def get_users_by_id(
    ids: Annotated[list[int], Query()],
    user_service: UserService = Depends(Provide[Container.user_service]),
    _: ClientCredentials = Security(
        Authorization,
        scopes=[Scopes.UsersRead.value],
    ),
) -> list[UserSchema]:
    return await user_service.get_users_by_id(ids)


@router.get("/{id}")
@inject
async def get_user_by_id(
    id: int,
    user_service: UserService = Depends(Provide[Container.user_service]),
    _: ClientCredentials = Security(
        Authorization,
        scopes=[Scopes.UsersRead.value],
    ),
) -> UserSchema | None:
    return await user_service.get_user_by_id(id)


@router.post("/")
@inject
async def create_user(
    user_create: UserCreateSchema,
    user_service: UserService = Depends(Provide[Container.user_service]),
    _: ClientCredentials = Security(
        Authorization,
        scopes=[Scopes.UsersWrite.value],
    ),
) -> UserSchema:
    return await user_service.create_user(user_create)


@router.patch("/{id}")
@inject
async def update_user(
    id: int,
    user_update: UserUpdateSchema,
    user_service: UserService = Depends(Provide[Container.user_service]),
    _: ClientCredentials = Security(
        Authorization,
        scopes=[Scopes.UsersWrite.value],
    ),
) -> UserSchema:
    return await user_service.update_user(id, user_update)
