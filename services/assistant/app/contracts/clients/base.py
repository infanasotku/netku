from abc import ABC, abstractmethod


class InternalBaseClient(ABC):
    @abstractmethod
    async def check_health(self) -> bool:
        """Checks health of service.

        :return: `True` if service available, `False` otherwise."""
