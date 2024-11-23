from abc import ABC, abstractmethod
from datetime import datetime

from app.repositories import XrayRepository
from app.clients.xray_client import XrayClient
from app.schemas.xray_schemas import XrayRecordCreateSchema, XrayRecordUpdateSchema


class AbstractXrayService(ABC):
    @abstractmethod
    async def restart_xray(self) -> str | None:
        pass

    @abstractmethod
    async def get_current_uid(self) -> str | None:
        pass


class XrayService(AbstractXrayService):
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
