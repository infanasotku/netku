from contextlib import asynccontextmanager
from fastapi import FastAPI

from common.logging import logger
from common.config import generate
from common.messaging.bus import MessageBus

from app.container import Container, init_pull
from app.infra.config import Settings
from app.contracts.services import ProxyService

from app.controllers import admin
from app.controllers import events


async def init_bus(container: Container) -> MessageBus:
    bus: MessageBus = await container.message_bus()
    scope_event = container.scope_event()
    info_event = container.info_event()
    terminated_event = container.terminated_event()
    hset_event = container.key_hset_event()
    expired_event = container.key_expired_event()

    auth_service = container.auth_service()
    proxy_service: ProxyService = await container.proxy_service()
    client_pull = container.engines_pull()

    state_changed_handler = events.ProxyStateChangedEventHandler(
        proxy_service, client_pull
    )
    engine_terminated_handler = events.ProxyEngineTerminatedEventHandler(
        proxy_service, client_pull
    )

    info_event.register_dispatcher(bus.process_out)
    terminated_event.register_dispatcher(bus.process_out)

    scope_event.register_handler(auth_service.process_update)
    hset_event.register_handler(state_changed_handler.handle)
    expired_event.register_handler(engine_terminated_handler.handle)

    bus.register_event(scope_event)
    bus.register_event(hset_event)
    bus.register_event(expired_event)

    return bus


def create_lifespan(container: Container):
    @asynccontextmanager
    async def lifespan(_):
        bus = None
        pull_context = None
        try:
            init = container.init_resources()
            if init is not None:
                await init

            pull_context = init_pull()
            bus = await init_bus(container)

            await pull_context.__aenter__()
            await bus.run()
            yield
        finally:
            if bus is not None and bus.running:
                await bus.stop()
            if pull_context is not None:
                await pull_context.__aexit__(None, None, None)

            shutdown = container.shutdown_resources()
            if shutdown is not None:
                await shutdown

    return lifespan


def create_app() -> FastAPI:
    settings = generate(Settings, logger)
    container = Container(logger=logger)
    container.config.from_pydantic(settings)
    rabbit_settings = {
        "rabbit_user": settings.rabbit_user,
        "rabbit_pass": settings.rabbit_pass,
        "rabbit_host": settings.rabbit_host,
        "rabbit_port": settings.rabbit_port,
    }
    container.rabbit_proxy_container.container.config.override(
        {"rabbit_vhost": settings.rabbit_proxy_vhost, **rabbit_settings}
    )
    container.rabbit_scope_container.container.config.override(
        {"rabbit_vhost": settings.rabbit_scope_vhost, **rabbit_settings}
    )
    container.wire(
        modules=[
            "app.controllers.admin.main",
            "app.controllers.admin.views",
            "app.container",
        ]
    )

    app = FastAPI(redoc_url=None, docs_url=None, lifespan=create_lifespan(container))
    app.container = container

    admin.register_admin(
        app,
        username=settings.admin_username,
        password=settings.admin_password,
    )

    return app


app = create_app()
