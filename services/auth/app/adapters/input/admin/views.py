from sqladmin import ModelView

import app.infra.database.models as models


class ClientScopeView(ModelView, model=models.ClientScope):
    can_export = False
    can_edit = False
    column_searchable_list = []

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
    can_export = False
    can_edit = False
    column_searchable_list = [models.Client.client_id]

    column_list = [models.Client.id, models.Client.client_id]
