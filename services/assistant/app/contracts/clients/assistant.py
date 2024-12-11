from abc import ABC, abstractmethod

from app.contracts.clients.base import BaseClient


class AssistantClient(BaseClient, ABC):
    @abstractmethod
    async def check_health(self) -> bool:
        """Checks health of assistant service.

        :return: `True` if assistant available, `False` otherwise."""
