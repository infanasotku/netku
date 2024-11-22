import asyncio
from abc import ABC, abstractmethod
from logging import Logger
from fastapi_utils.tasks import repeat_every


class Task(ABC):
    def __init__(self, name: str, restart_minutes: float, logger: Logger):
        self._task: asyncio.Task = None
        self.name = name
        self.logger = logger

        self._run = repeat_every(seconds=restart_minutes * 60, logger=logger)(self._run)

    def start(self) -> None:
        if self._task is not None:
            raise Exception(f"Task {self.name} already started.")
        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        if self._task is None:
            raise Exception(f"Task {self.name} already stopped.")
        self._task.cancel()
        await self._task
        self._task = None

    @abstractmethod
    async def _run(self):
        pass
