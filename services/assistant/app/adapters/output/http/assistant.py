import aiohttp

from app.contracts.clients.assistant import AssistantClient

from app.adapters.output.http.base import HTTPClient


class HTTPAssistantClient(HTTPClient, AssistantClient):
    def __init__(self, assistant_addr: str):
        self._assistant_addr = assistant_addr

    async def check_health(self) -> bool:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self._assistant_addr}/api/v1/health") as resp:
                    if resp.status == 200:
                        return True
                    return False
            except aiohttp.client_exceptions.ClientConnectorError:
                return False
