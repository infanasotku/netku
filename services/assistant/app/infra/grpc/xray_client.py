from abc import ABC, abstractmethod
from typing import Optional

from app.infra.grpc.gen.xray_pb2_grpc import XrayStub
from app.infra.grpc.gen.xray_pb2 import RestartResponse, Null

from app.infra.grpc.grpc_client import GRPCClient


class AbstractXrayClient(ABC):
    @abstractmethod
    async def restart(self) -> Optional[str]:
        """Sends grpc request to xray service for restart,
        obtains new uid.

        :return: New uid, if xray restarted, `None` otherwise.
        """
        pass


class XrayClient(GRPCClient, AbstractXrayClient):
    async def restart(self) -> Optional[str]:
        ch = await self.get_channel()
        if ch is None:
            return

        stub = XrayStub(ch)
        resp: RestartResponse = await stub.RestartXray(Null())
        return resp.uuid
