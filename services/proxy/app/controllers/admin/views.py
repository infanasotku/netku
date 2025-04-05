from logging import Logger
from uuid import UUID
from sqladmin import ModelView
from dependency_injector.wiring import Provide, inject

import app.infra.database.models as models
from app.contracts.services import ProxyService
from app.container import Container


class ProxyInfoView(ModelView, model=models.ProxyInfo):
    can_export = False
    can_edit = True
    can_delete = False
    can_create = False
    name_plural = "Proxy info"

    column_list = [
        models.ProxyInfo.uuid,
        models.ProxyInfo.key,
        models.ProxyInfo.addr,
        models.ProxyInfo.running,
        models.ProxyInfo.created,
    ]

    form_columns = [models.ProxyInfo.uuid]

    @inject
    async def update_model(
        self,
        request,
        pk,
        data,
        proxy_service: ProxyService = Provide[Container.proxy_service],
        logger: Logger = Provide[Container.logger],
    ):
        uuid = UUID(data["uuid"])
        info = await proxy_service.get_by_id(int(pk))

        if info.uuid != uuid:
            logger.info(f"Restarting engine [{info.key}].")
            await proxy_service.restart_engine(int(pk), uuid)
            logger.info(f"Engine [{info.key}] restarted.")
        # Workarround for custom updating.
        return models.ProxyInfo(
            uuid=uuid,
            created=info.created,
            addr=info.addr,
            running=info.running,
            key=info.key,
        )
