from abc import ABC, abstractmethod
import asyncio
from typing import Callable, Generic, TypeVar, Protocol

from common.schemas.base import BaseSchema


def _is_async_callable(obj) -> bool:
    return asyncio.iscoroutinefunction(obj) or (
        callable(obj) and asyncio.iscoroutinefunction(obj.__call__)
    )


EventDataT = TypeVar("EventDataT", bound=BaseSchema)


class EventSender(Protocol):
    def __call__(self, payload: str, *, name: str): ...


class BaseEvent(ABC, Generic[EventDataT]):
    name: str = "base"

    def register_handler(self, handler: Callable[[EventDataT], None]):
        self._handler = handler

    def register_dispatcher(self, sender: EventSender):
        self._dispatcher = sender

    async def handle(self, payload: str | dict):
        if self._handler is None:
            raise ValueError("Handler not specified")

        data = self.__class__._loads(payload)

        if _is_async_callable(self._handler):
            await self._handler(data)
        else:
            self._handler(data)

    async def dispatch(self, data: EventDataT):
        if self._dispatcher is None:
            raise ValueError("Sender not specified")

        dump = self.__class__._dumps(data)

        if _is_async_callable(self._dispatcher):
            await self._dispatcher(dump, name=self.name)
        else:
            self._dispatcher(dump, name=self.name)

    @staticmethod
    @abstractmethod
    def _dumps(data: EventDataT) -> str:
        pass

    @staticmethod
    @abstractmethod
    def _loads(payload: str | dict) -> EventDataT:
        pass
