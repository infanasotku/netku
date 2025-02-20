from uuid import UUID, uuid4

from common.grpc import BaseGRPCClient

from app.infra.grpc.gen.xray_pb2_grpc import XrayStub
from app.infra.grpc.gen.xray_pb2 import RestartResponse, RestartRequest
from app.contracts.clients import ProxyClient


class GRPCXrayClient(BaseGRPCClient, ProxyClient):
    service_name = "xray"

    async def restart(self, uuid: UUID | None = None) -> UUID | None:
        if uuid is None:
            uuid = uuid4()

        healthy = await self.check_health()
        if not healthy:
            return

        stub = XrayStub(self._channel)
        resp: RestartResponse = await stub.RestartXray(RestartRequest(uuid=str(uuid)))
        return UUID(resp.uuid)
