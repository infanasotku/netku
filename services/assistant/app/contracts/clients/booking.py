from abc import ABC, abstractmethod


class BookingClient(ABC):
    @abstractmethod
    async def run_booking(self, email: str, password: str) -> bool:
        """:return: `True` if booking ran, `False` otherwise."""

    @abstractmethod
    async def stop_booking(self, email: str, password: str):
        pass

    @abstractmethod
    async def booked(self, email: str, password: str) -> bool:
        pass
