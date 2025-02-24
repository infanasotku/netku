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
    can_delete = False
    name_plural = "Proxy info"

    column_list = [
        models.ProxyInfo.uuid,
        models.ProxyInfo.synced,
        models.ProxyInfo.running,
        models.ProxyInfo.last_update,
    ]

    form_columns = [models.ProxyInfo.uuid]

    @action(
        name="sync_with_xray",
        label="Sync with xray",
        add_in_detail=False,
    )
    @inject
    async def sync_with_xray(
        self,
        request: Request,
        proxy_service: ProxyService = Provide[Container.proxy_service],
    ):
        try:
            await proxy_service.sync_with_proxy()
        except ValueError:
            pass
        except RuntimeError:
            pass

        return RedirectResponse(request.url_for("admin:list", identity=self.identity))

    @inject
    async def insert_model(
        self,
        _,
        data,
        proxy_service: ProxyService = Provide[Container.proxy_service],
    ):
        uuid = UUID(data["uuid"])
        info = ProxyInfoCreateSchema(uuid=uuid)
        await proxy_service.create_proxy_info(info)
        # Workarround for custom creating.
        return models.ProxyInfo(
            uuid=info.uuid,
            last_update=info.last_update,
            synced=info.synced,
            running=info.running,
        )

    @inject
    async def update_model(
        self,
        request,
        pk,
        data,
        proxy_service: ProxyService = Provide[Container.proxy_service],
    ):
        uuid = UUID(data["uuid"])
        info = ProxyInfoUpdateSchema(uuid=uuid)
        old_info = await proxy_service.get_proxy_info()
        if old_info.uuid != info.uuid:
            await proxy_service.update_proxy_info(info)
            await proxy_service.sync_with_proxy()
        # Workarround for custom updating.
        return models.ProxyInfo(
            uuid=info.uuid,
            last_update=info.last_update,
            synced=info.synced,
            running=info.running,
        )

    @inject
    async def list(
        self,
        request,
        proxy_service: ProxyService = Provide[Container.proxy_service],
    ):
        await proxy_service.pull_from_proxy()
        return await super().list(request)
