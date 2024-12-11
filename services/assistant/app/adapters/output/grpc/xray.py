from app.contracts.clients import XrayClient

from app.adapters.output.grpc.gen.xray_pb2_grpc import XrayStub
from app.adapters.output.grpc.gen.xray_pb2 import RestartResponse, Null

from app.adapters.output.grpc.grpc import GRPCClient


class GRPCXrayClient(GRPCClient, XrayClient):
    service_name = "xray"

    async def restart(self) -> str | None:
        healthy = await self.check_health()
        if not healthy:
            return

        stub = XrayStub(self._channel)
        resp: RestartResponse = await stub.RestartXray(Null())
        return resp.uuid
