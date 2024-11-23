from app.contracts.clients import XrayClient as AbstractXrayClient

from app.infra.grpc.gen.xray_pb2_grpc import XrayStub
from app.infra.grpc.gen.xray_pb2 import RestartResponse, Null

from app.infra.grpc.grpc_client import GRPCClient


class XrayClient(GRPCClient, AbstractXrayClient):
    async def restart(self) -> str | None:
        ch = await self.get_channel()
        if ch is None:
            return

        stub = XrayStub(ch)
        resp: RestartResponse = await stub.RestartXray(Null())
        return resp.uuid
