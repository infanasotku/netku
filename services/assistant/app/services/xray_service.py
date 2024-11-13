from abc import ABC, abstractmethod
from datetime import datetime

from app.database.orm import AbstractRepository
from app.database.models import XrayRecord

from app.infra.grpc import AbstractXrayClient


class AbstractXrayService(ABC):
    @abstractmethod
    async def restart_xray(self) -> str | None:
        pass

    @abstractmethod
    async def get_current_uid(self) -> str | None:
        pass


class XrayService(AbstractXrayService):
    def __init__(self, repository: AbstractRepository, xray_client: AbstractXrayClient):
        self.repository = repository
        self.xray_client = xray_client

    async def restart_xray(self) -> str | None:
        uid = await self.xray_client.restart()

        if uid is None:
            return None

        xray_record = await self.repository.get_xray_record()

        if xray_record is None:
            await self.repository.create(
                XrayRecord(uid=uid, last_update=datetime.now())
            )
        else:
            xray_record.uid = uid
            xray_record.last_update = datetime.now()
            await self.repository.update(xray_record)

        return uid

    async def get_current_uid(self) -> str | None:
        xray_record = await self.repository.get_xray_record()

        if xray_record is not None:
            return xray_record.uid
