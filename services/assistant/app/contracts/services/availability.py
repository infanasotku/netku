from abc import ABC, abstractmethod

from app.schemas.availability import (
    AvailabilitySchema,
    Service,
)


class AvailabilityService(ABC):
    @abstractmethod
    async def check_availability(self, service: Service) -> AvailabilitySchema:
        """Checks availability of service.

        - Sends notify to telegram bot if service not available.
        - Logs service available status.

        :return: Logged availability record.
        """
