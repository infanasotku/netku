from abc import ABC, abstractmethod


class AssistantClient(ABC):
    @abstractmethod
    async def check_health(self) -> bool:
        """Checks health of assistant service.

        :return: `True` if assistant available, `False` otherwise."""
