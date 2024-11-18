from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable
from fastapi import FastAPI

from app.tasks import Task


class AbstractAppFactory(ABC):
    def __init__(self):
        self._tasks: list[Task] = []

    route_path: str

    @abstractmethod
    def create_app(self) -> FastAPI:
        """Creates fastapi app."""

    def create_lifespan(self) -> Callable[[FastAPI], AsyncGenerator]:
        """Creates fastapi lifespan."""

    def register_task(self, task: Task) -> None:
        self._tasks.append(task)

    def start_tasks(self) -> None:
        for task in self._tasks:
            task.start()

    async def stop_tasks(self) -> None:
        for task in self._tasks:
            await task.stop()


class AppFactory(AbstractAppFactory):
    def __init__(self):
        """Inits main app."""
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
            sub_factory.create_lifespan() for sub_factory in self._sub_factories
        ]

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator:
            generators = [lifespan(app) for lifespan in sub_lifespans]
            for generator in generators:
                await anext(generator)

            self.start_tasks()
            yield
            for generator in generators:
                await anext(generator)
            await self.stop_tasks()

        return lifespan
