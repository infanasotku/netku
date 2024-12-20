from abc import ABC, abstractmethod
from aiogram import Dispatcher


class BaseRouter(ABC):
    """Base class for registering router."""

    @abstractmethod
    def register_router(self, dp: Dispatcher):
        pass
