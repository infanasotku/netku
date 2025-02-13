import asyncio
from logging import Logger

from common.contracts.clients import MessageInClient, MessageOutClient
from common.logging import with_logging


class MessageBus:
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
        self._client_in = client_in
        self._client_out = client_out
        self._logger = logger
        self._task: asyncio.Task = None

        if client_in is not None:
            self._client_in.register(self._process_in)

    async def run(self):
        if self._client_in is None:
            raise ValueError("Messages-in client is not specified")

        if self._task is not None:
            raise RuntimeError("Bus already ran")

        self._task = asyncio.create_task(
            with_logging(self._client_in.run, self._logger)
        )

    async def stop(self):
        if self._task is None:
            raise ValueError("Bus already stopped")

        try:
            self._task.cancel()
            await self._task
        except asyncio.exceptions.CancelledError:
            pass

        self._task = None

    async def _process_in(self, msg: str):
        print(msg)
