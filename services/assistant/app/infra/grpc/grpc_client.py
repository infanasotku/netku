from typing import Awaitable, Callable, Optional, TypeAlias
from grpc import Channel

ChannelFactory: TypeAlias = Callable[[], Awaitable[Optional[Channel]]]


class GRPCClient:
    def __init__(self, get_channel: ChannelFactory) -> None:
        self.get_channel = get_channel
