from abc import ABC, abstractmethod
from datetime import datetime

from app.schemas.availability import (
    AvailabilitySchema,
    AvailabilityCreateSchema,
    Service,
)


class AvailabilityRepository(ABC):
    @abstractmethod
    async def log_availability(
        self, availability: AvailabilityCreateSchema
    ) -> AvailabilitySchema:
        """Logs availability record to DB.

        :return: Logged availability row.
        """

    @abstractmethod
    async def get_service_availability_factor_by_period(
        self, service_name: Service, start: datetime, end: datetime
    ) -> float:
        """Counts average availability factor for service
        for period from `start` to `end` in DB.

        :return: Counted factor.
        """
