import asyncio
from typing import Any, AsyncGenerator, Callable, Coroutine
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import grpc

from settings import settings, logger
from bot import tasks

from xray.gen.xray_pb2_grpc import XrayStub
from xray.gen.xray_pb2 import RestartResponse, Null

import health


def create_lifespan() -> Callable[["Xray", FastAPI], AsyncGenerator]:
    return Xray().lifespan


class Xray:
    def __init__(self):
        self._restart_minutes = settings.xray_restart_minutes
        self._xray_port = settings.xray_port
        self._xray_host = settings.xray_host
        self._reconnection_count = settings.xray_reconnection_count
        self._reconnection_delay = settings.xray_reconnection_delay

    async def lifespan(self, _: FastAPI) -> AsyncGenerator:
        restart_task = asyncio.create_task(self._run_restart_task())
        yield
        restart_task.cancel()
        self._stop()

    def _run_restart_task(self) -> Coroutine[Any, Any, None]:
        """Registers `self._restart` as repeat task.

        Returns:
        Wrapped `self._restart` task.
        """

        @repeat_every(seconds=self._restart_minutes * 60, logger=logger)
        async def restart():
            await self._restart()

        return restart()

    async def _restart(self):
        """Sends grpc request to xray service for restart,
        obtains new uid."""
        if not await self._check_health():
            return

        async with grpc.aio.insecure_channel(
            f"{self._xray_host}:{self._xray_port}"
        ) as ch:
            stub = XrayStub(ch)
            resp: RestartResponse = await stub.RestartXray(Null())
            await tasks.send_proxy_id(resp.uuid)

    async def _check_health(self) -> True:
        """Checks xray service health `self._reconnection_count` times
        with `self._reconnection_delay` delay.

        Returns:
        `True` if service health `False` otherwise.
        """
        for step in range(self._reconnection_count + 1):
            if step > 0:
                await asyncio.sleep(self._reconnection_delay)
                logger.warning(f"Attempting to reconnect to xray {step}...")
            if await health.check_xray():
                logger.info("Connection with xray established.")
                return True

        logger.error("Attempts to connect to xray failed.")
        return False
