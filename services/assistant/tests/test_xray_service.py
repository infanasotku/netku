from datetime import datetime
import pytest

from app.database.sql_db.models import XrayRecord
from app.database.sql_db.orm import ModelT
from app.services import XrayService
from app.clients.xray_client import XrayClient

from tests.stubs import StubRepository


class _StubXrayClient(XrayClient):
    def __init__(self, uid: str) -> None:
        self.uid = uid

    async def restart(self) -> str | None:
        return self.uid


class _StubRepository(StubRepository):
    def __init__(self):
        self.uid = None

    async def get_xray_record(self) -> XrayRecord | None:
        return XrayRecord(uid=self.uid, last_update=datetime.now())

    async def update(self, entity: ModelT) -> None:
        self.uid = entity.uid


@pytest.mark.parametrize("uid", ["test-uid1", "test-uid2"])
@pytest.mark.asyncio
async def test_restart_xray(uid: str):
    stub_xray_client = _StubXrayClient(uid)
    stub_repository = _StubRepository()

    xray_service = XrayService(stub_repository, stub_xray_client)
    await xray_service.restart_xray()

    assert uid == await xray_service.get_current_uid()
