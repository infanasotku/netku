from app.contracts.clients import XrayClient

from app.adapters.output.grpc.gen.xray_pb2_grpc import XrayStub
from app.adapters.output.grpc.gen.xray_pb2 import RestartResponse, Null

from app.adapters.output.grpc.grpc import GRPCClient


class GRPCXrayClient(GRPCClient, XrayClient):
    async def restart(self) -> str | None:
        ch = await self.get_channel()
        if ch is None:
            return

        stub = XrayStub(ch)
        resp: RestartResponse = await stub.RestartXray(Null())
        return resp.uuid
