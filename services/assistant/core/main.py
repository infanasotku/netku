from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable
from fastapi import FastAPI

from xray import xray
import bot


def create() -> FastAPI:
    """Creates core."""
    app = FastAPI(
        lifespan=create_lifespan(bot.create_lifespan(), xray.lifespan),
        docs_url=None,
        redoc_url=None,
    )
    _configure(app)
    return app


def _configure(app: FastAPI):
    "Mounts app services."
    app.mount(path="/bot", app=bot.create())


def create_lifespan(*lifespans: Callable) -> Callable[[FastAPI], AsyncGenerator]:
    """Creates core lifespan which handle `lifespans` of all app."""

    @asynccontextmanager
    async def _lifespan(app: FastAPI) -> AsyncGenerator:
        generators = [lifespan(app) for lifespan in lifespans]
        for generator in generators:
            await anext(generator)
        yield
        for generator in generators:
            await anext(generator)

    return _lifespan
