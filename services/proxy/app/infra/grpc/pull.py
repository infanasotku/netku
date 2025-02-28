from app.contracts.clients.proxy_engine import ProxyEngineClient


class ProxyClientPull:
    def __init__(self):
        self._pull: dict[str, ProxyEngineClient] = {}

    def register(self, id: str, client: ProxyEngineClient):
        self._pull[id] = client

    def delete(self, id):
        del self._pull[id]

    def get(self, id: str) -> ProxyEngineClient:
        return self._pull[id]
