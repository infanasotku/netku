import asyncio
from typing import Any, AsyncGenerator, Callable, Coroutine, Optional
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import uuid
import json

from subprocess import Popen, PIPE
from settings import settings, logger
from bot import tasks


def create_lifespan() -> Callable[["Xray", FastAPI], AsyncGenerator]:
    return Xray().lifespan


class Xray:
    def __init__(self):
        self._executable_dir = settings.xray_executable_dir
        self._executable_name = settings.xray_executable_name
        self._restart_minutes = settings.xray_restart_minutes
        self._xray_config = settings.xray_config
        self._inst: Optional[Popen] = None

        self._init_config()

    async def lifespan(self, _: FastAPI) -> AsyncGenerator:
        restart_task = asyncio.create_task(self._run_restart_task())
        yield
        restart_task.cancel()
        await self._stop()
        yield

    def _init_config(self):
        self._xray_config["inbounds"][0]["settings"]["fallbacks"][0]["dest"] = (
            settings.xray_fallback
        )
        self._xray_config["inbounds"][0]["streamSettings"]["tlsSettings"][
            "certificates"
        ][0]["certificateFile"] = settings.ssl_certfile
        self._xray_config["inbounds"][0]["streamSettings"]["tlsSettings"][
            "certificates"
        ][0]["keyFile"] = settings.ssl_keyfile
        self._xray_config["log"]["access"] = f"{settings.xray_config_dir}/access.log"
        self._xray_config["log"]["error"] = f"{settings.xray_config_dir}/error.log"

    async def _update_config(self):
        id = str(uuid.uuid4())
        self._xray_config["inbounds"][0]["settings"]["clients"][0]["id"] = id
        logger.info(f"New id: ({id}).")
        await tasks.send_proxy_id(id)

    def _run_restart_task(self) -> Coroutine[Any, Any, None]:
        @repeat_every(seconds=self._restart_minutes * 60, logger=logger)
        async def restart():
            await self._restart()

        return restart()

    async def _restart(self):
        self._stop()
        await self._update_config()
        self._start()

    def _stop(self):
        if self._inst:
            logger.info("Stopping xray.")
            try:
                self._inst.kill()
                self._inst = None
            except Exception as e:
                logger.warning(f"Xray starting failed: {e}")
                return
            logger.info("Xray stopped.")

    def _start(self):
        if not self._inst:
            logger.info("Starting xray.")
            try:
                self._inst = Popen(
                    [f"{self._executable_dir}/{self._executable_name}"],
                    stdin=PIPE,
                    stderr=PIPE,
                    text=True,
                )
                self._inst.communicate(json.dumps(self._xray_config))
            except Exception as e:
                logger.warning(f"Xray starting failed: {e}.")
                return
            logger.info("Xray started.")
