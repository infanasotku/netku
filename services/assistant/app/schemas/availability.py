from datetime import datetime
from enum import Enum
from pydantic import field_serializer

from app.schemas.base import BaseSchemaPK


class Service(Enum):
    booking = 1
    xray = 2
    assistant = 3


class AvailabilityCreateSchema(BaseSchemaPK):
    created: datetime
    service: Service
    availability_factor: float
    response_time: float

    @field_serializer("service")
    def serialize_service(self, value: Service) -> int:
        return value.value


class AvailabilitySchema(AvailabilityCreateSchema):
    pass
