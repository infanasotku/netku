from datetime import datetime

from app.contracts.services import XrayService
from app.contracts.repositories import XrayRepository
from app.contracts.clients.xray_client import XrayClient
from app.schemas.xray_schemas import XrayRecordCreateSchema, XrayRecordUpdateSchema


class XrayServiceImpl(XrayService):
    def __init__(self, xray_repository: XrayRepository, xray_client: XrayClient):
        self._xray_repository = xray_repository
        self._xray_client = xray_client

    async def restart_xray(self) -> str | None:
        uid = await self._xray_client.restart()

        if uid is None:
            return None

        xray_record = await self._xray_repository.get_last_xray_record()

        if xray_record is None:
            await self._xray_repository.create_xray_record(
                XrayRecordCreateSchema(uid=uid, last_update=datetime.now())
            )
        else:
            await self._xray_repository.update_xray_record(
                xray_record.id,
                XrayRecordUpdateSchema(uid=uid, last_update=datetime.now()),
            )

        return uid

    async def get_current_uid(self) -> str | None:
        xray_record = await self._xray_repository.get_last_xray_record()

        if xray_record is not None:
            return xray_record.uid
