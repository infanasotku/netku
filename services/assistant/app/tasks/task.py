from abc import ABC, abstractmethod
import asyncio


class Task(ABC):
    def __init__(self, name: str):
        self._task: asyncio.Task = None
        self.name = name

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
