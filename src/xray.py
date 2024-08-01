import asyncio
import logging
from typing import Any, AsyncGenerator, Coroutine, Optional
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from subprocess import Popen
import settings


def create() -> FastAPI:
    xray = Xray()
    return FastAPI(docs_url=None, redoc_url=None, lifespan=xray.lifespan)


class Xray:
    def __init__(self):
        self._executable_dir = settings.get().xray_executable_dir
        self._executable_name = settings.get().xray_executable_name
        self._restart_minutes = settings.get().xray_restart_minutes
        self._inst: Optional[Popen] = None

    async def lifespan(self, _: FastAPI) -> AsyncGenerator:
        restart_task = asyncio.create_task(self._run_restart_task())
        yield
        restart_task.cancel()
        yield

    def _run_restart_task(self) -> Coroutine[Any, Any, None]:
        @repeat_every(seconds=self._restart_minutes * 60, logger=logging.getLogger("uvicorn.error"))
        def restart():
            self._restart()

        return restart()

    def _restart(self):
        self._stop()
        self._start()

    def _stop(self):
        if self._inst:
            logging.getLogger("uvicorn.error").info("Stopping xray")
            try:
                self._inst.kill()
                self._inst = None
            except Exception as e:
                logging.getLogger("uvicorn.error").warning(f"Xray starting failed: {e}")
                return
            logging.getLogger("uvicorn.error").info("Xray stopped")
    
    def _start(self):
        if not self._inst:
            logging.getLogger("uvicorn.error").info("Starting xray")
            try:
                self._inst = Popen([f"{self._executable_dir}/{self._executable_name}"])
            except Exception as e:
                logging.getLogger("uvicorn.error").warning(f"Xray starting failed: {e}")
                return
            logging.getLogger("uvicorn.error").info("Xray started")
