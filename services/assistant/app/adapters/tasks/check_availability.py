from logging import Logger
from celery import Celery

from app.contracts.services import AvailabilityService
from app.contracts.protocols import CreateService

from app.adapters.tasks.task import CeleryTask
from app.schemas.availability import Service


class CheckAvailabilityTask(CeleryTask):
    def __init__(
        self,
        logger: Logger,
        celery: Celery,
        create_availability_service: CreateService[AvailabilityService],
        services: list[Service],
    ):
        super().__init__("check_availability", logger, celery)
        self._create_availability_service = create_availability_service
        self._services = services

    async def _run(self):
        self._logger.info("Availability subscription performing.")

        async with self._create_availability_service() as a_service:
            for service in self._services:
                await a_service.check_availability(service, notify_factor_level=0.3)

        self._logger.info("Availability subscription performed.")
