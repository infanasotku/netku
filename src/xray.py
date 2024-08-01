import asyncio
import logging
from typing import Any, AsyncGenerator, Coroutine
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every, NoArgsNoReturnAsyncFuncT
import subprocess as sub
import settings


def create() -> FastAPI:
    xray = Xray()
    return FastAPI(docs_url=None, redoc_url=None, lifespan=xray.lifespan)


class Xray:
    def __init__(self):
        self._executable_dir = settings.get().xray_executable_dir
        # self._inst = sub.Popen()

    async def lifespan(self, _: FastAPI) -> AsyncGenerator:
        restart_task = asyncio.create_task(self._run_restart_task())
        yield
        restart_task.cancel()
        yield

    def _run_restart_task(self) -> Coroutine[Any, Any, None]:
        @repeat_every(seconds=5, logger=logging.getLogger("uvicorn.error"))
        def restart():
            self._restart()

        return restart()

    def _restart(self):
        print(f"hello! {self._executable_dir}")
