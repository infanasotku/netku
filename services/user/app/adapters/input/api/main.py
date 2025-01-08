from fastapi import FastAPI

from app.adapters.input.api.router import router


def create_api() -> FastAPI:
    api = FastAPI()

    api.include_router(router, prefix="/users")

    return api
