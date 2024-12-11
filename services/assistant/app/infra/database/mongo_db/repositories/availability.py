from app.contracts.repositories import AvailabilityRepository

from app.schemas.availability import (
    AvailabilityCreateSchema,
    AvailabilitySchema,
)

from app.infra.database.mongo_db.repositories.base import MongoBaseRepository
from app.infra.database.mongo_db.orm import result_to_schema


class MongoAvailabilityRepository(AvailabilityRepository, MongoBaseRepository):
    collection_name = "availabilities"

    async def get_availability_by_id(self, id: int) -> AvailabilitySchema | None:
        availability = await self._collection.find_one({"_id": id})

        if availability is None:
            return None

        return result_to_schema(availability, AvailabilitySchema)

    async def log_availability(
        self, availability: AvailabilityCreateSchema
    ) -> AvailabilitySchema:
        dump = availability.model_dump(exclude_unset=True)
        inserted_result = await self._collection.insert_one(dump)

        return await self.get_availability_by_id(inserted_result.inserted_id)
