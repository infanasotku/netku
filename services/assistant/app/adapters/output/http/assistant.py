from app.contracts.clients.assistant import AssistantClient

from app.adapters.output.http.base import HTTPClient


class HTTPAssistantlient(HTTPClient, AssistantClient):
    def __init__(self, assistant_addr: str):
        self._assistant_addr = assistant_addr

    async def check_health(self) -> bool:
        raise NotImplementedError
