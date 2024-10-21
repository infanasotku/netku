from typing import Optional

from infra.grpc.gen.xray_pb2_grpc import XrayStub
from infra.grpc.gen.xray_pb2 import RestartResponse, Null

from infra.grpc.grpc_client import GRPCClient


class XrayClient(GRPCClient):
    async def restart(self) -> Optional[str]:
        """Sends grpc request to xray service for restart,
        obtains new uid.

        :return: New uid, if xray restarted, `None` otherwise.
        """
        ch = await self.get_channel()
        if ch is None:
            return

        stub = XrayStub(ch)
        resp: RestartResponse = await stub.RestartXray(Null())
        return resp.uuid
