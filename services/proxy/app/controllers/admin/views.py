from datetime import datetime
from uuid import UUID
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView, action
from dependency_injector.wiring import Provide, inject

import app.infra.database.models as models
from app.contracts.services import ProxyService
from app.container import Container
from app.schemas.proxy import ProxyInfoCreateSchema, ProxyInfoUpdateSchema


class ProxyInfoView(ModelView, model=models.ProxyInfo):
    can_export = False
    can_edit = True
    name_plural = "Proxy info"

    column_list = [models.ProxyInfo.uuid, models.ProxyInfo.last_update]

    form_columns = [models.ProxyInfo.uuid]

    @action(
        name="sync_with_xray",
        label="Sync with xray",
        add_in_detail=False,
    )
    async def sync_with_xray(self, request: Request):
        print("Hello!")

        return RedirectResponse(request.url_for("admin:list", identity=self.identity))

    @inject
    async def insert_model(
        self,
        _,
        data,
        proxy_service: ProxyService = Provide[Container.proxy_service],
    ):
        uuid = UUID(data["uuid"])
        info = ProxyInfoCreateSchema(last_update=datetime.now(), uuid=uuid)
        await proxy_service.create_proxy_info(info)
        # Workarround for custom creating.
        return models.ProxyInfo(last_update=info.last_update, uuid=info.uuid)

    @inject
    async def update_model(
        self,
        request,
        pk,
        data,
        proxy_service: ProxyService = Provide[Container.proxy_service],
    ):
        uuid = UUID(data["uuid"])
        info = ProxyInfoUpdateSchema(last_update=datetime.now(), uuid=uuid)
        await proxy_service.update_proxy_info(info)
        # Workarround for custom updating.
        return models.ProxyInfo(last_update=info.last_update, uuid=info.uuid)
