import grpc

from settings import settings, logger

from health.gen.health_pb2_grpc import HealthStub
from health.gen.health_pb2 import HealthCheckRequest, HealthCheckResponse


async def check_xray() -> bool:
    async with grpc.aio.insecure_channel(
        f"{settings.xray_host}:{settings.xray_port}"
    ) as ch:
        stub = HealthStub(ch)
        try:
            resp: HealthCheckResponse = await stub.Check(
                HealthCheckRequest(service="xray")
            )
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return False
            logger.error(f"Failed to check xray health: {e}")

        return (
            True if resp.status == HealthCheckResponse.ServingStatus.SERVING else False
        )
