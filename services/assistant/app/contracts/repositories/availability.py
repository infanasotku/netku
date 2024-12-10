from abc import ABC, abstractmethod

from app.schemas.availability import AvailabilitySchema, AvailabilityCreateSchema


class AvailabilityRepository(ABC):
    @abstractmethod
    async def log_availability(
        self, availability: AvailabilityCreateSchema
    ) -> AvailabilitySchema:
        """Logs availability record to DB.

        :return: Logged availability row.
        """
