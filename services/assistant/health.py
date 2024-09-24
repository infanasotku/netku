from grpc_health.v1.health_pb2 import HealthCheckRequest, HealthCheckResponse
from grpc_health.v1.health_pb2_grpc import HealthStub
import grpc

from settings import logger


async def check_serivce(name: str, addr: str) -> bool:
    """Checks health of `name` service at `addr` address.
    Returns:
    `True` if service health, `False` otherwise.
    """
    async with grpc.aio.insecure_channel(addr) as ch:
        stub = HealthStub(ch)
        try:
            resp: HealthCheckResponse = await stub.Check(
                HealthCheckRequest(service=name)
            )
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                return False
            logger.error(f"Failed to check {name} health: {e}")
            return False

        return (
            True if resp.status == HealthCheckResponse.ServingStatus.SERVING else False
        )
