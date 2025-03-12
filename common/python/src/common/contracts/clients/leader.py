from abc import abstractmethod

from common.contracts.clients.base import BaseClient


class LeaderElector(BaseClient):
    """Implementation int of leader election pattern."""

    @abstractmethod
    async def try_acquire_leadership(self) -> bool:
        """Try to acquire leadership with limited ttl.
        Returns:
            `True` if leadership acquired, `False` otherwise.
        """
