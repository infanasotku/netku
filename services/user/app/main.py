from collections.abc import Iterable
from fastapi import FastAPI
from typing import NamedTuple


class AppConfig(NamedTuple):
    app: FastAPI
    route: str


def create_app(sub_apps: Iterable[AppConfig] | None = None) -> FastAPI:
    if sub_apps is None:
        sub_apps = []

    app = FastAPI(
        docs_url=None,
        redoc_url=None,
    )
    for app_info in sub_apps:
        app.mount(app_info.route, app_info.app)

    return app
