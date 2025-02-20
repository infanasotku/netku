from common.contracts.event import BaseEvent
from common.schemas.proxy import ProxyInfo


class ProxyUUIDChangedEvent(BaseEvent[ProxyInfo]):
    name = "proxy.uuid.changed"

    @staticmethod
    def _dumps(data):
        return data.model_dump_json()

    @staticmethod
    def _loads(payload):
        if isinstance(payload, str):
            return ProxyInfo.model_validate_json(payload)
        return ProxyInfo.model_validate(payload)
