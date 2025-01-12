from sqladmin import ModelView

import app.infra.database.models as models


class UserView(ModelView, model=models.User):
    can_export = False
    can_edit = False
    column_searchable_list = [models.User.phone_number]

    column_list = [models.User.id, models.User.phone_number, models.User.telegram_id]
