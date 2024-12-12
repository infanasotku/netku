from grpc import StatusCode
from grpc.aio import AioRpcError, Channel

from grpc_health.v1.health_pb2 import HealthCheckRequest, HealthCheckResponse
from grpc_health.v1.health_pb2_grpc import HealthStub


class GRPCClient:
    service_name: str = "grpc"

    def __init__(self, channel: Channel) -> None:
        self._channel = channel

    async def check_health(self) -> bool:
        stub = HealthStub(self._channel)
        try:
            resp: HealthCheckResponse = await stub.Check(
                HealthCheckRequest(service=self.service_name)
            )
        except AioRpcError as e:
            if e.code() == StatusCode.UNAVAILABLE:
                return False
            return False

        return (
            True if resp.status == HealthCheckResponse.ServingStatus.SERVING else False
        )
