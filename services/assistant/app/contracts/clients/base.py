from abc import ABC, abstractmethod


class BaseClient(ABC):
    pass


class InternalBaseClient(BaseClient):
    @abstractmethod
    async def check_health(self) -> bool:
        """Checks health of service.

        :return: `True` if service available, `False` otherwise."""
