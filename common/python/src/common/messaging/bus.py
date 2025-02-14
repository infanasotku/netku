from enum import Enum
from functools import partial
from logging import Logger
import asyncio
import json
import logging
import traceback
import uuid

from common.contracts.bus import BaseMessageBus
from common.contracts.clients import MessageInClient, MessageOutClient
from common.logging import with_logging


class EventType(Enum):
    In = 1
    Out = 2


class MessageBus(BaseMessageBus):
    """
    Bus for handling input and output application message.
    """

    def __init__(
        self,
        logger: Logger,
        *,
        client_in: MessageInClient = None,
        client_out: MessageOutClient = None,
    ):
        super().__init__()
        self._client_in = client_in
        self._client_out = client_out
        self._logger = logger
        self._task: asyncio.Task = None
        self._id = 0
        self._id_lock = asyncio.Lock()

        if client_in is not None:
            self._client_in.register(self.process_in)

    async def process_in(self, message, *, headers):
        id = await self._get_id()
        log = partial(self._log, id=id, type=EventType.In)
        info = partial(log, level=logging.INFO)
        warning = partial(log, level=logging.WARNING)
        error = partial(log, level=logging.ERROR)

        info("Recieved event.")

        if "x-event-name" not in headers:
            warning("Event name not specified.")
            return

        event_name = headers["x-event-name"]

        if event_name not in self._events:
            warning(f"Event [{event_name}] not found.")
            return

        info(f"Handling [{event_name}] event.")
        try:
            event = self._events[event_name]
            await event.handle(message)
        except Exception:
            error(
                "\n".join(
                    [
                        f"Error occured while processing [{event_name}] event:",
                        traceback.format_exc(),
                    ]
                )
            )
            return
        info(f"Event {event_name} completed.")

    async def process_out(self, payload: str, *, name: str):
        log = partial(self._log, id=None, type=EventType.Out)
        info = partial(log, level=logging.INFO)

        info(f"Sending [{name}] event.")
        data = {"event": name, "payload": payload}
        dump = json.dumps(data)
        await self._client_out.send(dump)
        info(f"Event [{name}] sended.")

    async def run(self):
        if self._client_in is None:
            raise ValueError("Messages-in client is not specified")

        if self._task is not None:
            raise RuntimeError("Bus already ran")

        self._task = asyncio.create_task(
            with_logging(self._client_in.run, self._logger)
        )
        self._logger.info("Bus started.")

    async def stop(self):
        if self._task is None:
            raise ValueError("Bus already stopped.")

        try:
            self._logger.info("Bus stopping.")
            self._task.cancel()
            await self._task
        except asyncio.exceptions.CancelledError:
            pass

        self._logger.info("Bus stopped.")
        self._task = None

    async def _get_id(self):
        async with self._id_lock:
            return str(uuid.uuid4())

    def _log(
        self,
        msg: str,
        *,
        level: int,
        type: EventType,
        id: str | None = None,
    ):
        type_msg = "[BUS-IN]" if type == EventType.In else "[BUS-OUT]"
        id_msg = "" if type == EventType.Out else f"[{id}]"
        wrapped_msg = f"{type_msg}{id_msg}: {msg}"
        self._logger.log(level, wrapped_msg)
