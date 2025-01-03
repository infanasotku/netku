from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine

from app.adapters.input.admin.auth import AdminAuthenticationBackend
import app.adapters.input.admin.views as views


def register_admin(app: FastAPI, *, engine: AsyncEngine, username: str, password: str):
    authentication_backend = AdminAuthenticationBackend(
        username=username, password=password
    )
    admin = Admin(
        app,
        engine,
        title="Auth admin panel",
        authentication_backend=authentication_backend,
    )
    admin.add_view(views.ClientScopeView)
    admin.add_view(views.ScopeView)
    admin.add_view(views.ClientView)
