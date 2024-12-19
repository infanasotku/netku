from logging import Logger
from celery import Celery

from app.contracts.services import UserService, XrayService
from app.contracts.protocols import CreateService

from app.adapters.tasks.task import CeleryTask


class RestartProxyTask(CeleryTask):
    def __init__(
        self,
        logger: Logger,
        celery: Celery,
        create_user_service: CreateService[UserService],
        create_xray_service: CreateService[XrayService],
    ):
        super().__init__("restart_proxy", logger, celery)
        self.create_user_service = create_user_service
        self.create_xray_service = create_xray_service

    async def _run(self):
        """Restarts proxy and sends `id` to all user subscripted to proxy."""
        self._logger.info("Proxy subscription performing.")

        async with self.create_xray_service() as xray:
            uid = await xray.restart_xray()

        if not uid:
            self._logger.warning("Proxy subscription failed - xray didn't restarted.")
            return

        async with self.create_user_service() as service:
            title = "New generated proxy id:"
            body = f"/{uid}/"
            await service.send_notify_by_subscriptions(
                ["proxy_subscription"],
                "\n".join([title, body]),
            )

        self._logger.info("Proxy subscription performed.")
