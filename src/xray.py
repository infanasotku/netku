from typing import AsyncGenerator
from fastapi import FastAPI
import subprocess as sub
import settings


def create() -> FastAPI:
    xray = Xray()
    app = FastAPI(docs_url=None, redoc_url=None, lifespan=xray.lifespan)


class Xray:
    def __init__(self):
        self._executable_dir = settings.get().xray_executable_dir
        self._inst = sub.Popen()

    def lifespan(self, _: FastAPI) -> AsyncGenerator:
        pass

    def restart_xray(self):
        pass
