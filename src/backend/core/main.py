from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable
from fastapi import FastAPI

import xray


def create() -> FastAPI:
    app = FastAPI(
        lifespan=create_lifespan(xray.create_lifespan()), docs_url=None, redoc_url=None
    )
    _configure(app)
    return app


def _configure(app: FastAPI):
    pass


def create_lifespan(*lifespans: Callable) -> Callable[[Any], AsyncGenerator]:
    @asynccontextmanager
    async def _lifespan(app: FastAPI) -> AsyncGenerator:
        generators = [lifespan(app) for lifespan in lifespans]
        for generator in generators:
            await anext(generator)
        yield
        for generator in generators:
            await anext(generator)

    return _lifespan
