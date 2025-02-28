from common.contracts.event import BaseEvent
from common.schemas.proxy import ProxyInfoSchema


class ProxyInfoChangedEvent(BaseEvent[ProxyInfoSchema]):
    name = "proxy.info.changed"

    @staticmethod
    def _dumps(data):
        return data.model_dump_json()

    @staticmethod
    def _loads(payload):
        if isinstance(payload, str):
            return ProxyInfoSchema.model_validate_json(payload)
        return ProxyInfoSchema.model_validate(payload)


class ProxyTerminatedEvent(BaseEvent[ProxyInfoSchema]):
    name = "proxy.terminated"

    @staticmethod
    def _dumps(data):
        return data.model_dump_json()

    @staticmethod
    def _loads(payload):
        if isinstance(payload, str):
            return ProxyInfoSchema.model_validate_json(payload)
        return ProxyInfoSchema.model_validate(payload)
