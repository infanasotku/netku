from abc import ABC
from typing import Any

from common.contracts.event import BaseEvent


class BaseMessageBus(ABC):
    def __init__(self):
        self._events: dict[str, BaseEvent] = {}

    async def process_in(self, message: str, *, headers: dict[str, Any]):
        """Processes input message as event."""

    async def process_out(self, payload: str, *, name: str):
        """Send output message with `payload`."""

    def register_event(self, event: BaseEvent):
        self._events[event.name] = event
        event.register_sender(self.process_out)
