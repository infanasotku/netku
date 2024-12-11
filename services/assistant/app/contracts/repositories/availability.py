from abc import ABC, abstractmethod

from app.schemas.availability import (
    AvailabilitySchema,
    AvailabilityCreateSchema,
    Service,
)


class AvailabilityRepository(ABC):
    @abstractmethod
    async def get_availability_by_id(self, id: int) -> AvailabilitySchema | None:
        """Receives from DB availability record by specified id.

        :return: Received record if it existm `None` otherwise.
        """

    @abstractmethod
    async def log_availability(
        self, availability: AvailabilityCreateSchema
    ) -> AvailabilitySchema:
        """Logs availability record to DB.

        :return: Logged availability row.
        """

    @abstractmethod
    async def get_average_service_availability_factor(self, service: Service) -> float:
        """Counts average availability factor of service.

        :return: Counted factor.
        """

    @abstractmethod
    async def get_availabilities_by_service(
        self, service: Service
    ) -> list[AvailabilitySchema]:
        """Receives from DB all availability records for specified service.

        :return: Received records.
        """
