from typing import Optional
import grpc

from settings import settings
import health

from xray.gen.xray_pb2_grpc import XrayStub
from xray.gen.xray_pb2 import RestartResponse, Null


class Xray:
    def __init__(self):
        self.uid: str = None

    async def restart(self) -> Optional[str]:
        """Sends grpc request to xray service for restart,
        obtains new uid.
        Returns:
        New uid, if xray restarted, `None` otherwise.
        """
        if not await health.wait_healthy(
            "xray", f"{settings.xray_host}:{settings.xray_port}"
        ):
            return

        async with grpc.aio.insecure_channel(
            f"{settings.xray_host}:{settings.xray_port}"
        ) as ch:
            stub = XrayStub(ch)
            resp: RestartResponse = await stub.RestartXray(Null())
            self.uid = resp.uuid
            return resp.uuid
