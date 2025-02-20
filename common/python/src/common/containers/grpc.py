from logging import Logger
from typing import Any, AsyncGenerator
from grpc.aio import Channel, secure_channel, insecure_channel
import grpc


async def get_channel(
    ssl_certfile: str | None = None,
    *,
    host: str,
    port: int,
    logger: Logger | None = None,
) -> AsyncGenerator[Channel, Any]:
    addr = f"{host}:{port}"

    if ssl_certfile is not None:
        with open(ssl_certfile, "rb") as f:
            cert = f.read()
        creds = grpc.ssl_channel_credentials(cert)
        channel = secure_channel(addr, creds)
    else:
        channel = insecure_channel(addr)
        if logger is not None:
            logger.warning("[GRPC] Using insecure credentials.")

    yield channel
    await channel.close()
