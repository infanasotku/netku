from abc import ABC, abstractmethod
from logging import Logger
import asyncio

from celery import Celery
from celery.app.task import Task


class CeleryTask(ABC):
    def __init__(self, name: str, logger: Logger, celery: Celery):
        self._name = name
        self._logger = logger
        self._celery = celery

        @self._celery.task
        def start():
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self._run())

        self.task: Task = start

    @abstractmethod
    async def _run(self):
        pass
