from fastapi import APIRouter

from common.contracts.protocols import CreateService
from app.contracts.services import ClientService

from app.adapters.input.api.auth.token import TokenRouter


class AuthRouter:
    def __init__(self, create_client_service: CreateService[ClientService]):
        self._create_client_service = create_client_service

        self.router = APIRouter()

        token = TokenRouter(create_client_service)

        self.router.include_router(token.router, prefix="/token")
