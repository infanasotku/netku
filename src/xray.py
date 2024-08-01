import asyncio
import logging
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import subprocess as sub
import settings


def create() -> FastAPI:
    xray = Xray()
    return FastAPI(docs_url=None, redoc_url=None, lifespan=xray.lifespan)


class Xray:
    def __init__(self):
        self._executable_dir = settings.get().xray_executable_dir
        self._inst = sub.Popen()

    async def lifespan(self, _: FastAPI) -> AsyncGenerator:
        restart_task = asyncio.create_task(self.restart())
        yield
        restart_task.cancel()
        yield

    @repeat_every(seconds=5, logger=logging.getLogger("uvicorn.error"))
    def restart(self):
        print(f"hello! {self._executable_dir}")
