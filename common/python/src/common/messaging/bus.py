from enum import Enum
from functools import partial
from logging import Logger
import asyncio
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
        *clients_in: MessageInClient,
        client_out: MessageOutClient = None,
    ):
        super().__init__()
        self._clients_in = clients_in
        self._client_out = client_out
        self._logger = logger
        self._tasks: list[asyncio.Task] = []
        self._id = 0
        self._id_lock = asyncio.Lock()

        for client_in in self._clients_in:
            client_in.register(self.process_in)

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
        await self._client_out.send(payload, headers={"x-event-name": name})
        info(f"Event [{name}] sended.")

    async def run(self):
        if len(self._clients_in) == 0:
            raise ValueError("Messages-in client is not specified")

        if len(self._tasks) != 0:
            raise RuntimeError("Bus already ran")

        for client_in in self._clients_in:
            task = asyncio.create_task(with_logging(client_in.run, self._logger))
            self._tasks.append(task)
        self._logger.info("Bus started.")

    async def stop(self):
        if len(self._tasks) == 0:
            raise ValueError("Bus already stopped.")

        self._logger.info("Bus stopping.")
        for task in self._tasks:
            try:
                task.cancel()
                await task
            except asyncio.exceptions.CancelledError:
                continue

        self._logger.info("Bus stopped.")
        self._tasks = []

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
