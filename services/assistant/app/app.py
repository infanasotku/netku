from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from logging import Logger
from typing import AsyncGenerator, Callable
from fastapi import FastAPI


class AbstractAppFactory(ABC):
    route_path: str

    def __init__(self, logger: Logger):
        self._logger = logger

    @abstractmethod
    def create_app(self) -> FastAPI:
        """Creates fastapi app."""

    def create_lifespan(self) -> Callable[[FastAPI], AsyncGenerator]:
        """Creates fastapi lifespan."""


class AppFactory(AbstractAppFactory):
    def __init__(self, logger: Logger):
        """Inits main app."""
        super().__init__(logger)
        self._sub_factories: list[AbstractAppFactory] = []

    def register_sub_factory(self, sub_factory: AbstractAppFactory):
        self._sub_factories.append(sub_factory)

    def create_app(self) -> FastAPI:
        app = FastAPI(
            lifespan=self.create_lifespan(),
            docs_url=None,
            redoc_url=None,
        )

        for sub_factory in self._sub_factories:
            app.mount(sub_factory.route_path, sub_factory.create_app())

        return app

    def create_lifespan(self) -> Callable[[FastAPI], AsyncGenerator]:
        """Creates core lifespan which handle `lifespans` of all app."""
        sub_lifespans = [
            lifespan
            for lifespan in (
                sub_factory.create_lifespan() for sub_factory in self._sub_factories
            )
            if lifespan
        ]

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator:
            generators = [lifespan(app) for lifespan in sub_lifespans]
            self._logger.info("Starting lifespans.")
            for generator in generators:
                await anext(generator)
            self._logger.info("Starting lifespans finished.")
            yield
            for generator in generators:
                await anext(generator)

        return lifespan
