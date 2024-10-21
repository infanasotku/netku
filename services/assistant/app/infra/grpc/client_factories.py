from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from grpc import StatusCode
from grpc.aio import insecure_channel, AioRpcError, Channel

from grpc_health.v1.health_pb2 import HealthCheckRequest, HealthCheckResponse
from grpc_health.v1.health_pb2_grpc import HealthStub

from infra.grpc.grpc_client import GRPCClient, CreateChannel
from infra.grpc.booking_client import BookingClient
from infra.grpc.xray_client import XrayClient


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

    async def _create_channel(self) -> Optional[Channel]:
        """Creates grpc channel.

        :return:
            `Channel` if grpc service healthy and ready for requests.
            `None` otherwise.
        """
        channel = insecure_channel(f"{self.client_addr}:{self.client_port}")
        # Checks grcp service health
        if not await self._check_health(channel):
            return

        return channel

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[GRPCClient, None]:
        """Creates corresponding instance of `GRPCClient`.

        :return: Initiated grpc client.
        """
        channel: Channel = None

        # Cached version of `self._create_channel`
        async def create_channel() -> Optional[Channel]:
            nonlocal channel
            if channel is not None:
                return channel
            channel = await self._create_channel()
            return channel

        yield self._init_client(create_channel)

        if channel is not None:
            await channel.close()

    @abstractmethod
    def _init_client(self, create_channel: CreateChannel) -> GRPCClient:
        """Innits grpc client with needed params."""
        pass


class XrayClientFactory(ClientFactory):
    def _init_client(self, create_channel: CreateChannel) -> XrayClient:
        return XrayClient(create_channel)


class BookingClientFactory(ClientFactory):
    def _init_client(self, create_channel: CreateChannel) -> BookingClient:
        return BookingClient(create_channel)
