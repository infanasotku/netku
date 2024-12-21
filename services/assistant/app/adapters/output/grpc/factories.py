from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from grpc.aio import Channel, secure_channel
import grpc

from app.adapters.output.grpc.booking import GRPCBookingClient
from app.adapters.output.grpc.base import GRPCClient
from app.adapters.output.grpc.xray import GRPCXrayClient


class GRPCClientFactory(ABC):
    """Specifies factory for grpc clients."""

    def __init__(self, client_addr: str, client_port: int, ssl_certfile: str):
        self.client_addr = client_addr
        self.client_port = client_port
        self.ssl_certfile = ssl_certfile

    def _create_channel(self) -> Channel:
        """:return: created grpc channel."""
        with open(self.ssl_certfile, "rb") as f:
            cert = f.read()

        credentials = grpc.ssl_channel_credentials(cert)

        addr = f"{self.client_addr}:{self.client_port}"
        channel = secure_channel(addr, credentials)

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
