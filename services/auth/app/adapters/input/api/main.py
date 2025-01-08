from fastapi import FastAPI

from app.adapters.input.api.auth import AuthRouter


def create_api() -> FastAPI:
    api = FastAPI()

    auth = AuthRouter()

    api.include_router(auth.router, prefix="/auth")

    return api
