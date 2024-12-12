from abc import ABC, abstractmethod

from app.schemas.availability import (
    AvailabilitySchema,
    Service,
)


class AvailabilityService(ABC):
    @abstractmethod
    async def check_availability(
        self,
        service: Service,
        retries_count: int = 10,
        notify_factor_level: float = 0.5,
    ) -> AvailabilitySchema:
        """Checks availability of service.

        - Sends notify to telegram bot if service not available.
        - Logs service available status.

        :param retries_count: count of availability checks for counts availability factor.
        :param notify_factor_level: minimal level for sending notify to telegram bot.

        :return: Logged availability record.
        """
