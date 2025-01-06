from fastapi import FastAPI

from common.contracts.protocols import CreateService
from app.contracts.services import ClientService

from app.adapters.input.api.auth import AuthRouter


def create_api(create_client_service: CreateService[ClientService]) -> FastAPI:
    api = FastAPI(root_path="/api")

    auth = AuthRouter(create_client_service)

    api.include_router(auth.router, prefix="/auth")

    return api
