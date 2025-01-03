from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine


from app.adapters.input.admin.auth import AdminAuthenticationBackend


def register_admin(app: FastAPI, *, engine: AsyncEngine, username: str, password: str):
    authentication_backend = AdminAuthenticationBackend(
        username=username, password=password
    )
    return Admin(
        app,
        engine,
        title="Auth admin panel",
        authentication_backend=authentication_backend,
    )
