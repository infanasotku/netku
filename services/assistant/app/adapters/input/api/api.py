from fastapi import FastAPI

from app.app import AbstractAppFactory
from app.adapters.input.api.info.router import INFORouter


class APIAppFactory(AbstractAppFactory):
    def __init__(self, logger):
        super().__init__(logger)
        self.route_path = "/api"

    def create_app(self):
        api = FastAPI()

        main_router = INFORouter()

        api.include_router(main_router.router, prefix="/info")

        return api
