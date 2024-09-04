import asyncio
from typing import Any, AsyncGenerator, Callable, Coroutine
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import grpc

from settings import settings, logger
from bot import tasks

from xray.handler.h_pb2_grpc import HandlerServiceStub
from xray.handler.handler_pb2 import RestartResponse, Null


def create_lifespan() -> Callable[["Xray", FastAPI], AsyncGenerator]:
    return Xray().lifespan


class Xray:
    def __init__(self):
        self._restart_minutes = settings.xray_restart_minutes
        self._xray_port = settings.xray_port
        self._xray_host = settings.xray_host

    async def lifespan(self, _: FastAPI) -> AsyncGenerator:
        restart_task = asyncio.create_task(self._run_restart_task())
        yield
        restart_task.cancel()
        self._stop()

    def _init_config(self):
        # self._xray_config["inbounds"][0]["settings"]["fallbacks"][0]["dest"] = (
        #     settings.xray_fallback
        # )
        # self._xray_config["inbounds"][0]["streamSettings"]["tlsSettings"][
        #     "certificates"
        # ][0]["certificateFile"] = settings.ssl_certfile
        # self._xray_config["inbounds"][0]["streamSettings"]["tlsSettings"][
        #     "certificates"
        # ][0]["keyFile"] = settings.ssl_keyfile
        # self._xray_config["log"]["access"] = f"{settings.xray_config_dir}/access.log"
        # self._xray_config["log"]["error"] = f"{settings.xray_config_dir}/error.log"
        # self._xray_config["inbounds"][0]["settings"]["clients"][0]["id"] = id
        pass

    def _run_restart_task(self) -> Coroutine[Any, Any, None]:
        @repeat_every(seconds=self._restart_minutes * 60, logger=logger)
        async def restart():
            await self._restart()

        return restart()

    async def _restart(self):
        """Sends grpc request to xray service for restart,
        obtains new uid.
        """
        print(f"{self._xray_host}:{self._xray_host}")
        with grpc.insecure_channel(f"{self._xray_host}:{self._xray_port}") as ch:
            stub = HandlerServiceStub(ch)
            resp: RestartResponse = stub.RestartXray(Null())

            id = resp.uuid
            print(id)

        # await tasks.send_proxy_id(id)
