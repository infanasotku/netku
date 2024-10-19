from typing import Awaitable, Callable, Optional, TypeAlias
from grpc import Channel

ChannelFactory: TypeAlias = Callable[[], Awaitable[Optional[Channel]]]


class GRPCClient:
    def __init__(self, channel_factory: ChannelFactory) -> None:
        self.channel_factory = channel_factory
