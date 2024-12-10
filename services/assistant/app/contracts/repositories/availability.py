from abc import ABC, abstractmethod

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
    async def get_average_service_availability_factor(
        self, service_name: Service
    ) -> float:
        """Counts average availability factor of service.

        :return: Counted factor.
        """
