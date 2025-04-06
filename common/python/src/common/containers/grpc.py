from logging import Logger
from typing import Any, AsyncGenerator
from grpc.aio import Channel, secure_channel, insecure_channel
import grpc
import certifi


async def get_channel(
    with_cert=True,
    *,
    host: str,
    port: int,
    logger: Logger | None = None,
) -> AsyncGenerator[Channel, Any]:
    addr = f"{host}:{port}"

    if with_cert:
        with open(certifi.where(), "rb") as f:
            cert = f.read()
        creds = grpc.ssl_channel_credentials(cert)
        channel = secure_channel(addr, creds)
    else:
        channel = insecure_channel(addr)
        if logger is not None:
            logger.warning("[GRPC] Using insecure credentials.")

    yield channel
    await channel.close()
