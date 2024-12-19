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
        notify_factor_level: float,
    ):
        super().__init__("check_availability", logger, celery)
        self._create_availability_service = create_availability_service
        self._services = services
        self._notify_factor_level = notify_factor_level

    async def _run(self):
        self._logger.info("Availability subscription performing.")

        async with self._create_availability_service() as a_service:
            for service in self._services:
                availability = await a_service.check_availability(
                    service, notify_factor_level=self._notify_factor_level
                )
                if availability.availability_factor <= self._notify_factor_level:
                    self._logger.warning(
                        f"Availability subscription: [{service.name}] is not available."
                    )

        self._logger.info("Availability subscription performed.")
