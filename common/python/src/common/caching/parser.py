from abc import ABC, abstractmethod
from typing import Any
import json


class Parser(ABC):
    def __init__(self):
        self.headers: dict[str, Any] = {}
        self.message = ""

    @abstractmethod
    def __call__(self, data: str, channel: str):
        pass


class KeyEventParser(Parser):
    def __call__(self, data, channel):
        self.message = json.dumps({"key": data})

        event_type = channel.split(":")[1]

        self.headers = {"x-event-name": f"keyevent.{event_type}"}
