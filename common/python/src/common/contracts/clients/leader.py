from abc import abstractmethod

from common.contracts.clients.base import BaseClient


class LeaderElectionClient(BaseClient):
    """Implementation int of leader election pattern."""

    def __init__(self, expiration: int):
        """
        Args:
            expiration (int): leadership expiration in seconds.
        """
        self._expiration = expiration

    @abstractmethod
    async def try_acquire_leadership(self, acquire_id: str) -> bool:
        """Try to acquire leadership with limited ttl.
        Returns:
            `True` if leadership acquired, `False` otherwise.
        """
