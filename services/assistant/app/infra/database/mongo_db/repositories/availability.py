from app.contracts.repositories import AvailabilityRepository

from app.schemas.availability import (
    AvailabilityCreateSchema,
    AvailabilitySchema,
    Service,
)

from app.infra.database.mongo_db.repositories.base import MongoBaseRepository
from app.infra.database.mongo_db.orm import result_to_schema


class MongoAvailabilityRepository(AvailabilityRepository, MongoBaseRepository):
    collection_name = "availabilities"

    async def log_availability(
        self, availability: AvailabilityCreateSchema
    ) -> AvailabilitySchema:
        dump = availability.model_dump(exclude_unset=True)
        inserted_result = await self._collection.insert_one(dump)

        return await self.get_availability_by_id(inserted_result.inserted_id)

    async def get_average_service_availability_factor(self, service: Service) -> float:
        pipeline = [
            {"$match": {"service": service.value}},
            {
                "$group": {
                    "_id": "$service",
                    "totalFactor": {"$sum": "$availability_factor"},
                    "count": {"$sum": 1},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "averageFactor": {"$divide": ["$totalFactor", "$count"]},
                }
            },
        ]

        async_list = await self._collection.aggregate(pipeline)
        list = await async_list.to_list()

        return list[0]["averageFactor"]

    async def get_availability_by_id(self, id: int) -> AvailabilitySchema | None:
        availability = await self._collection.find_one({"_id": id})

        if availability is None:
            return None

        return result_to_schema(availability, AvailabilitySchema)

    async def get_availabilities_by_service(
        self, service: Service
    ) -> list[AvailabilitySchema]:
        availabilities = self._collection.find({"service": service.value})

        return [
            result_to_schema(availability, AvailabilitySchema)
            async for availability in availabilities
        ]
