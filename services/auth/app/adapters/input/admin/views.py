from sqladmin import ModelView

from app.contracts.clients import SecurityClient
from common.contracts.protocols import CreateClient

import app.infra.database.models as models


class ClientScopeView(ModelView, model=models.ClientScope):
    can_export = False
    can_edit = False
    column_searchable_list = []

    column_list = [
        models.ClientScope.id,
        models.ClientScope.client,
        models.ClientScope.scope,
    ]

    form_ajax_refs = {
        "scope": {
            "fields": ("name",),
            "order_by": "id",
        },
        "client": {
            "fields": ("client_id",),
            "order_by": "id",
        },
    }


class ScopeView(ModelView, model=models.Scope):
    can_export = False
    can_edit = False
    column_searchable_list = [models.Scope.name]

    column_list = [models.Scope.id, models.Scope.name]


class ClientView(ModelView, model=models.Client):
    create_security_client: CreateClient[SecurityClient]

    can_export = False
    can_edit = False
    column_searchable_list = [models.Client.client_id]

    column_list = [models.Client.id, models.Client.client_id]

    async def on_model_change(
        self, data: dict, model: models.Client, is_created, request
    ):
        async with ClientView.create_security_client() as security:
            if (
                "hashed_client_secret" in data
                and data["hashed_client_secret"] != model.hashed_client_secret
            ):
                data["hashed_client_secret"] = security.get_hash(
                    data["hashed_client_secret"]
                )
