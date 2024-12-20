from abc import abstractmethod

from app.schemas.availability import (
    AvailabilitySchema,
    AvailabilityCreateSchema,
)

from app.contracts.repositories.base import BaseRepository


class AvailabilityRepository(BaseRepository):
    @abstractmethod
    async def get_availability_by_id(self, id: int) -> AvailabilitySchema | None:
        """Receives from DB availability record by specified id.

        :return: Received record if it existm `None` otherwise.
        """

    @abstractmethod
    async def log_availability(
        self, availability_create: AvailabilityCreateSchema
    ) -> AvailabilitySchema:
        """Logs availability record to DB.

        :return: Logged availability row.
        """
