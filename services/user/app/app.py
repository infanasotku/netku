from collections.abc import Iterable
from fastapi import FastAPI


def create_app(sub_apps: Iterable[tuple[FastAPI, str]] | None = None) -> FastAPI:
    if sub_apps is None:
        sub_apps = []

    app = FastAPI(
        docs_url=None,
        redoc_url=None,
    )
    for subapp, route in sub_apps:
        app.mount(route, subapp)

    return app
