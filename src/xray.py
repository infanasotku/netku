import asyncio
import logging
from typing import Any, AsyncGenerator, Coroutine, Optional
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import uuid
import json

from subprocess import Popen, PIPE
import settings


def create() -> FastAPI:
    xray = Xray()
    return FastAPI(docs_url=None, redoc_url=None, lifespan=xray.lifespan)


class Xray:

    def __init__(self):
        self._executable_dir = settings.get().xray_executable_dir
        self._executable_name = settings.get().xray_executable_name
        self._restart_minutes = settings.get().xray_restart_minutes
        self._xray_config = settings.get().xray_config
        self._logger = logging.getLogger("uvicorn.error")
        self._inst: Optional[Popen] = None

        self._init_config()

    async def lifespan(self, _: FastAPI) -> AsyncGenerator:
        restart_task = asyncio.create_task(self._run_restart_task())
        yield
        restart_task.cancel()
        yield

    def _init_config(self):
        self._xray_config["inbounds"][0]["settings"]["fallbacks"][0]["dest"] = settings.get().xray_fallback
        self._update_config()

    def _update_config(self):
        self._xray_config["inbounds"][0]["settings"]["clients"][0]["id"] = str(uuid.uuid4())

    def _run_restart_task(self) -> Coroutine[Any, Any, None]:
        @repeat_every(seconds=self._restart_minutes * 60, logger=self._logger)
        def restart():
            self._restart()

        return restart()

    def _restart(self):
        self._stop()
        self._update_config()
        self._start()

    def _stop(self):
        if self._inst:
            self._logger.info("Stopping xray")
            try:
                self._inst.kill()
                self._inst = None
            except Exception as e:
                self._logger.warning(f"Xray starting failed: {e}")
                return
            self._logger.info("Xray stopped")
    
    def _start(self):
        if not self._inst:
            self._logger.info("Starting xray")
            try:
                self._inst = Popen([f"{self._executable_dir}/{self._executable_name}"], stdin=PIPE, stderr=PIPE, text=True)
                self._inst.communicate(json.dumps(self._xray_config))
            except Exception as e:
                self._logger.warning(f"Xray starting failed: {e}")
                return
            self._logger.info("Xray started")
