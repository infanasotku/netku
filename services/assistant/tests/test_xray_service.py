from typing import Optional
from datetime import datetime
import pytest

from app.database.models import XrayRecord
from app.services import XrayService
from app.infra.grpc import AbstractXrayClient

from tests.stubs import StubRepository


class _StubXrayClient(AbstractXrayClient):
    def __init__(self, uid: str) -> None:
        self.uid = uid

    async def restart(self) -> Optional[str]:
        return self.uid


class _StubRepository(StubRepository):
    def __init__(self):
        self.uid = None

    async def get_xray_record(self) -> Optional[XrayRecord]:
        return XrayRecord(uid=self.uid, last_update=datetime.now())

    async def update_xray_record(self, uid: str) -> None:
        self.uid = uid


@pytest.mark.parametrize("uid", ["test-uid1", "test-uid2"])
@pytest.mark.asyncio
async def test_restart_xray(uid: str):
    stub_xray_client = _StubXrayClient(uid)
    stub_repository = _StubRepository()

    xray_service = XrayService(stub_repository, stub_xray_client)
    await xray_service.restart_xray()

    assert uid == await xray_service.get_current_uid()
