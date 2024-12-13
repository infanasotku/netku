from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from grpc.aio import insecure_channel, Channel

from app.adapters.output.grpc.booking import GRPCBookingClient
from app.adapters.output.grpc.base import GRPCClient
from app.adapters.output.grpc.xray import GRPCXrayClient


class GRPCClientFactory(ABC):
    """Specifies factory for grpc clients."""

    def __init__(
        self,
        client_addr: str,
        client_port: int,
        reconnection_delay: float,
    ):
        self.client_addr = client_addr
        self.client_port = client_port
        self.reconnection_delay = reconnection_delay

    def _create_channel(self) -> Channel:
        """:return: created grpc channel."""
        channel = insecure_channel(f"{self.client_addr}:{self.client_port}")

        return channel

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[GRPCClient, None]:
        """Creates corresponding instance of `GRPCClient`.

        :return: Initiated grpc client.
        """
        channel = self._create_channel()

        yield self._init_client(channel)

        if channel is not None:
            await channel.close()

    @abstractmethod
    def _init_client(self, channel: Channel) -> GRPCClient:
        """Innits grpc client with needed params."""


class GRPCXrayClientFactory(GRPCClientFactory):
    def _init_client(self, channel: Channel) -> GRPCXrayClient:
        return GRPCXrayClient(channel)


class GRPCBookingClientFactory(GRPCClientFactory):
    def _init_client(self, channel: Channel) -> GRPCBookingClient:
        return GRPCBookingClient(channel)
