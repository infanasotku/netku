from typing import AsyncGenerator, Callable
from fastapi import FastAPI


def create() -> FastAPI:
    bot = FastAPI(docs_url=None, redoc_url=None)
    _configure(bot)
    return bot


def create_lifespan() -> Callable[[FastAPI], AsyncGenerator]:
    pass


def _configure(app: FastAPI):
    pass
