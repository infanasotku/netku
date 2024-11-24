import pytest
from datetime import datetime

from app.services.xray import XrayServiceImpl
from app.contracts.clients.xray import XrayClient
from app.schemas.xray import (
    XrayRecordCreateSchema,
    XrayRecordSchema,
    XrayRecordUpdateSchema,
)

from tests.stubs import StubXrayRepository


class _StubXrayClient(XrayClient):
    def __init__(self, uid: str) -> None:
        self.uid = uid

    async def restart(self) -> str | None:
        return self.uid


class _StubRepository(StubXrayRepository):
    def __init__(self):
        self.uid = None

    async def get_last_xray_record(self) -> XrayRecordSchema | None:
        if self.uid is None:
            return None
        return XrayRecordSchema(uid=self.uid, last_update=datetime.now())

    async def update_xray_record(
        self, user_id: int, user_update: XrayRecordUpdateSchema
    ) -> XrayRecordSchema:
        self.uid = user_update.uid

    async def create_xray_record(
        self, account_create: XrayRecordCreateSchema
    ) -> XrayRecordSchema:
        self.uid = account_create.uid


@pytest.mark.parametrize(
    "uid",
    ["3e2c1c6e-b6fe-486e-9d84-07f932b3590e", "d42c4276-cbd8-4203-9be3-e9071ffdb44e"],
)
@pytest.mark.asyncio
async def test_restart_xray(uid: str):
    stub_xray_client = _StubXrayClient(uid)
    stub_repository = _StubRepository()

    xray_service = XrayServiceImpl(stub_repository, stub_xray_client)
    await xray_service.restart_xray()

    assert uid == await xray_service.get_current_uid()
