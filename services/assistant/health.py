import asyncio
from grpc_health.v1.health_pb2 import HealthCheckRequest, HealthCheckResponse
from grpc_health.v1.health_pb2_grpc import HealthStub
import grpc

from settings import logger, settings


async def check_service(name: str, addr: str) -> bool:
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


async def wait_healthy(name: str, addr: str) -> True:
    """Checks service health `settings.reconnection_retries` times
    with `settings.reconnection_delay` delay.

    Returns:
    `True` if service health `False` otherwise.
    """
    for step in range(settings.reconnection_retries + 1):
        if step > 0:
            await asyncio.sleep(settings.reconnection_delay)
            logger.warning(f"Attempting to reconnect to xray {step}...")
        if await check_service(name, addr):
            logger.info("Connection with xray established.")
            return True

    logger.error("Attempts to connect to xray failed.")
    return False
