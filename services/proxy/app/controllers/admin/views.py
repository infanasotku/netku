from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView, action

import app.infra.database.models as models


class ProxyInfoView(ModelView, model=models.ProxyInfo):
    can_export = False
    can_edit = True
    name_plural = "Proxy info"

    column_list = [models.ProxyInfo.uuid, models.ProxyInfo.last_update]

    @action(
        name="restart_xray",
        label="Restart xray",
        add_in_detail=True,
    )
    async def approve_worker_bid(self, request: Request):
        print("Hello!")

        return RedirectResponse(request.url_for("admin:list", identity=self.identity))
