from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from grpc import StatusCode
from grpc.aio import insecure_channel, AioRpcError, Channel

from grpc_health.v1.health_pb2 import HealthCheckRequest, HealthCheckResponse
from grpc_health.v1.health_pb2_grpc import HealthStub

from app.adapters.output.grpc.booking import GRPCBookingClient
from app.adapters.output.grpc.grpc import GRPCClient, CreateChannel
from app.adapters.output.grpc.xray import GRPCXrayClient


class ClientFactory(ABC):
    """Specifies factory for grpc clients."""

    def __init__(
        self,
        client_addr: str,
        client_port: int,
        service_name: str,
        reconnection_delay: float,
    ):
        self.client_addr = client_addr
        self.client_port = client_port
        self.grpc_service_name = service_name
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

    async def _create_channel(self) -> Channel | None:
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
        async def create_channel() -> Channel | None:
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


class XrayClientFactory(ClientFactory):
    def _init_client(self, create_channel: CreateChannel) -> GRPCXrayClient:
        return GRPCXrayClient(create_channel)


class BookingClientFactory(ClientFactory):
    def _init_client(self, create_channel: CreateChannel) -> GRPCBookingClient:
        return GRPCBookingClient(create_channel)
