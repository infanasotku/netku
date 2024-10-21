from typing import Awaitable, Callable, Optional, TypeAlias
from grpc import Channel

CreateChannel: TypeAlias = Callable[[], Awaitable[Optional[Channel]]]


class GRPCClient:
    def __init__(self, get_channel: CreateChannel) -> None:
        self.get_channel = get_channel
