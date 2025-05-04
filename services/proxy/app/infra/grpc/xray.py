from uuid import UUID, uuid4

from common.grpc import BaseGRPCClient

from app.infra.grpc.gen.xray_pb2_grpc import XrayStub
from app.infra.grpc.gen.xray_pb2 import XrayInfo
from app.contracts.clients import ProxyEngineClient


class GRPCXrayClient(BaseGRPCClient, ProxyEngineClient):
    service_name = "xray"

    async def restart(self, uuid: UUID | None = None):
        if uuid is None:
            uuid = uuid4()

        stub = XrayStub(self._channel)
        resp: XrayInfo = await stub.RestartXray(XrayInfo(uuid=str(uuid)))
        return UUID(resp.uuid)
