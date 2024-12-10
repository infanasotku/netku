import datetime
from enum import Enum

from app.schemas.base import BaseSchemaPK


class Service(Enum):
    booking = 1
    xray = 2
    assistant = 3


class AvailabilityCreateSchema(BaseSchemaPK):
    created: datetime
    service_name: Service
    availability_factor: float


class AvailabilitySchema(AvailabilityCreateSchema):
    pass
