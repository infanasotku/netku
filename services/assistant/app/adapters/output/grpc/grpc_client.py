from typing import Awaitable, Callable, TypeAlias
from grpc import Channel

CreateChannel: TypeAlias = Callable[[], Awaitable[Channel | None]]


class GRPCClient:
    def __init__(self, get_channel: CreateChannel) -> None:
        self.get_channel = get_channel
