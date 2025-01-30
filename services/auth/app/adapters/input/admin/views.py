from contextlib import AbstractAsyncContextManager
from sqladmin import ModelView
from dependency_injector.wiring import Provide, inject


from app.contracts.services import ClientService
from common.contracts.clients import SecurityClient
from app.container import Container
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

    async def delete_model(
        self,
        request,
        pk,
        client_service_context: AbstractAsyncContextManager[ClientService] = Provide[
            Container.client_service
        ],
    ):
        async with client_service_context as client_service:
            await client_service.remove_client_scope(int(pk))


class ScopeView(ModelView, model=models.Scope):
    can_export = False
    can_edit = False
    column_searchable_list = [models.Scope.name]

    column_list = [models.Scope.id, models.Scope.name]


class ClientView(ModelView, model=models.Client):
    can_export = False
    can_edit = False
    column_searchable_list = [models.Client.client_id]

    column_list = [models.Client.id, models.Client.client_id]

    @inject
    async def on_model_change(
        self,
        data: dict,
        model: models.Client,
        is_created,
        request,
        security_client: SecurityClient = Provide[Container.security_client],
    ):
        if (
            "hashed_client_secret" in data
            and data["hashed_client_secret"] != model.hashed_client_secret
        ):
            data["hashed_client_secret"] = security_client.get_hash(
                data["hashed_client_secret"]
            )
