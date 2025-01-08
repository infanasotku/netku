from fastapi import APIRouter

from app.adapters.input.api.auth.token import TokenRouter


class AuthRouter:
    def __init__(self):
        self.router = APIRouter()

        token = TokenRouter()

        self.router.include_router(token.router, prefix="/token")
