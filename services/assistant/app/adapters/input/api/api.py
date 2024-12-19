from fastapi import FastAPI

from app.app import AbstractAppFactory
from app.adapters.input.api.v1.router import MainAPIRouter


class APIAppFactory(AbstractAppFactory):
    def __init__(self, logger):
        super().__init__(logger)
        self.route_path = "/api"

    def create_app(self):
        api = FastAPI()

        main_router = MainAPIRouter()

        api.include_router(main_router.router, prefix="/v1")

        return api
