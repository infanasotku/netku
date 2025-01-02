from fastapi import FastAPI

from common.contracts.protocols import CreateService
from app.contracts.services import UserService

from app.adapters.input.api.router import UserRouter


def create_api(create_user_service: CreateService[UserService]) -> FastAPI:
    api = FastAPI()

    user = UserRouter(create_user_service)

    api.include_router(user.router)

    return api
