from app.contracts.clients.proxy import ProxyClient


class ProxyClientPull:
    def __init__(self):
        self._pull: dict[str, ProxyClient] = {}

    def register(self, id: str, client: ProxyClient):
        self._pull[id] = client

    def delete(self, id):
        del self._pull[id]

    def get(self, id: str) -> ProxyClient:
        return self._pull[id]
