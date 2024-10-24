from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable
from fastapi import FastAPI


class AbstractAppFactory(ABC):
    route_path: str

    @abstractmethod
    def create_app(self) -> FastAPI:
        """Creates fastapi app."""

    def create_lifespan(self) -> Callable[[FastAPI], AsyncGenerator]:
        """Creates fastapi lifespan."""


class AppFactory(AbstractAppFactory):
    def __init__(self, *sub_factories: AbstractAppFactory):
        """Inits main app.
        :param get_db: DB async session factory.
        """
        self.sub_factories = sub_factories

    def create_app(self) -> FastAPI:
        app = FastAPI(
            lifespan=self.create_lifespan(),
            docs_url=None,
            redoc_url=None,
        )

        for sub_factory in self.sub_factories:
            app.mount(sub_factory.route_path, sub_factory.create_app())

        return app

    def create_lifespan(self) -> Callable[[FastAPI], AsyncGenerator]:
        """Creates core lifespan which handle `lifespans` of all app."""
        sub_lifespans = [
            sub_factory.create_lifespan() for sub_factory in self.sub_factories
        ]

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator:
            generators = [lifespan(app) for lifespan in sub_lifespans]
            for generator in generators:
                await anext(generator)
            yield
            for generator in generators:
                await anext(generator)

        return lifespan
