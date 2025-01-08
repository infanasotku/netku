from fastapi import FastAPI

from app.adapters.input.api import auth


def create_api() -> FastAPI:
    api = FastAPI()

    api.include_router(auth.router, prefix="/auth")

    return api
