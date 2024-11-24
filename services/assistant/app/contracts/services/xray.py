from abc import ABC, abstractmethod


class XrayService(ABC):
    @abstractmethod
    async def restart_xray(self) -> str | None:
        pass

    @abstractmethod
    async def get_current_uid(self) -> str | None:
        pass
