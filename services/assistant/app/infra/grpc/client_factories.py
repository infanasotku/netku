from abc import ABC, abstractmethod
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from grpc import StatusCode
from grpc.aio import insecure_channel, AioRpcError, Channel

from grpc_health.v1.health_pb2 import HealthCheckRequest, HealthCheckResponse
from grpc_health.v1.health_pb2_grpc import HealthStub

from infra.grpc.grpc_client import GRPCClient, ChannelFactory


class ClientFactory(ABC):
    """Specifies factory for grpc clients."""

    def __init__(
        self,
        client_addr: str,
        client_port: int,
        service_name: str,
        reconnection_retries: int,
        reconnection_delay: float,
    ):
        self.client_addr = client_addr
        self.client_port = client_port
        self.grpc_service_name = service_name
        self.reconnection_retries = reconnection_retries
        self.reconnection_delay = reconnection_delay

    async def _check_health(self, channel: Channel) -> bool:
        """Checks health of grpc service.

        :return: `True` if service health, `False` otherwise.
        """
        stub = HealthStub(channel)
        try:
            resp: HealthCheckResponse = await stub.Check(
                HealthCheckRequest(service=self.grpc_service_name)
            )
        except AioRpcError as e:
            if e.code() == StatusCode.UNAVAILABLE:
                return False
            return False

        return (
            True if resp.status == HealthCheckResponse.ServingStatus.SERVING else False
        )

    async def _wait_healthy(self, channel: Channel) -> True:
        """Checks service health `self.reconnection_retries` times
        with `self.reconnection_delay` delay.

        :return: `True` if service health `False` otherwise.
        """
        for step in range(self.reconnection_retries + 1):
            if step > 0:
                await asyncio.sleep(self.reconnection_delay)
            if await self._check_health(channel):
                return True

        return False

    async def _create_channel(self, check_immediate: bool = False) -> Optional[Channel]:
        """Creates grpc channel.

        :param check_immediate: Specifies service health checking.
            If `True` - service will check one time, otherwise
            service will check `self.reconnection_retries` times.

        :return:
            `Channel` if grpc service available and ready for requests.
            `None` otherwise.
        """
        channel = insecure_channel(f"{self.client_addr}:{self.client_port}")
        # Checks grcp service health
        if (
            check_immediate and not await self._check_health(channel)
        ) or not await self._wait_healthy(channel):
            return

        return channel

    @asynccontextmanager
    async def create(
        self, check_immediate: bool = False
    ) -> AsyncGenerator[GRPCClient, None]:
        """Creates corresponding instance of `GRPCClient`.

        :param check_immediate: Specifies service health checking.
            If `True` - service will check one time, otherwise
            service will check `self.reconnection_retries` times.

        :return: Initiated grpc client.
        """
        channel: Channel = None

        async def channel_factory() -> Optional[Channel]:
            nonlocal channel
            if channel is not None:
                return channel
            channel = await self._create_channel(check_immediate)
            return channel

        yield self._init_client(channel_factory)

        if channel is not None:
            await channel.close()

    @abstractmethod
    def _init_client(self, channel_factory: ChannelFactory) -> GRPCClient:
        """Additional innits grpc client with needed params."""
        pass
