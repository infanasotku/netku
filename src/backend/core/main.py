from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable
from fastapi import FastAPI

import xray


def create() -> FastAPI:
    """Creates core."""
    app = FastAPI(
        lifespan=create_lifespan(xray.create_lifespan()), docs_url=None, redoc_url=None
    )
    return app


def create_lifespan(*lifespans: Callable) -> Callable[[Any], AsyncGenerator]:
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
