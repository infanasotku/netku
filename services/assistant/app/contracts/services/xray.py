from abc import abstractmethod

from app.contracts.services.base import BaseService


class XrayService(BaseService):
    @abstractmethod
    async def restart_xray(self) -> str | None:
        pass

    @abstractmethod
    async def get_current_uid(self) -> str | None:
        pass
