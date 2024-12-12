from abc import ABC, abstractmethod

from app.contracts.clients.base import InternalBaseClient


class BookingClient(InternalBaseClient, ABC):
    @abstractmethod
    async def run_booking(self, email: str, password: str) -> bool:
        """:return: `True` if booking ran, `False` otherwise."""

    @abstractmethod
    async def stop_booking(self, email: str, password: str):
        pass

    @abstractmethod
    async def booked(self, email: str, password: str) -> bool:
        pass
