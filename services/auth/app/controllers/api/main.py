from fastapi import FastAPI

from app.controllers.api import router as auth


def create_api() -> FastAPI:
    api = FastAPI()

    api.include_router(auth.router, prefix="/auth")

    return api
