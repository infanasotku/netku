from typing import Optional
from database.orm import AbstractRepository

from infra.grpc.xray_client import XrayClient


class XrayService:
    def __init__(self, repository: AbstractRepository, xray_client: XrayClient):
        self.repository = repository
        self.xray_client = xray_client

    async def restart_xray(self) -> Optional[str]:
        uid = await self.xray_client.restart()

        if uid is not None:
            await self.repository.update_xray_record(uid)

        return uid

    async def get_current_uid(self) -> Optional[str]:
        xray_record = await self.repository.get_xray_record()

        if xray_record is not None:
            return xray_record.uid
