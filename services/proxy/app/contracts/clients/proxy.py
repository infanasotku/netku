from abc import abstractmethod
from uuid import UUID
from typing import NamedTuple

from common.contracts.clients import RemoteBaseClient


class EngineInfo(NamedTuple):
    uuid: UUID | None
    running: bool


class ProxyClient(RemoteBaseClient):
    @abstractmethod
    async def restart(self, uuid: UUID | None = None) -> UUID | None:
        """Sends request to proxy for restart.

        If `uuid` not specified - restarts proxy with random uuid.

        Returns:
            New uuid, if proxy restarted, `None` otherwise.
        """

    @abstractmethod
    async def get_engine_info(self) -> EngineInfo:
        """Checks info of proxy engine."""
