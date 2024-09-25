import asyncio
from typing import Any, AsyncGenerator, Coroutine
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import grpc

from settings import settings, logger
import health
from bot import tasks

from xray.gen.xray_pb2_grpc import XrayStub
from xray.gen.xray_pb2 import RestartResponse, Null


class Xray:
    def __init__(self):
        self.uid: str = None

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

        @repeat_every(seconds=settings.xray_restart_minutes * 60, logger=logger)
        async def restart():
            await self._restart()

        return restart()

    async def _restart(self):
        """Sends grpc request to xray service for restart,
        obtains new uid."""
        if not await health.wait_healthy(
            "xray", f"{settings.xray_host}:{settings.xray_port}"
        ):
            return

        async with grpc.aio.insecure_channel(
            f"{settings.xray_host}:{settings.xray_port}"
        ) as ch:
            stub = XrayStub(ch)
            resp: RestartResponse = await stub.RestartXray(Null())
            await tasks.send_proxy_id(resp.uuid)
