from common.schemas import BaseSchema
from common.events.proxy import BaseEvent


class KeyEventSchema(BaseSchema):
    key: str


class KeyHSetEvent(BaseEvent[KeyEventSchema]):
    name = "keyevent.hset"

    @staticmethod
    def _dumps(data):
        return data.model_dump_json()

    @staticmethod
    def _loads(payload):
        if isinstance(payload, str):
            return KeyEventSchema.model_validate_json(payload)
        return KeyEventSchema.model_validate(payload)


class KeyExpiredEvent(BaseEvent[KeyEventSchema]):
    name = "keyevent.expired"

    @staticmethod
    def _dumps(data):
        return data.model_dump_json()

    @staticmethod
    def _loads(payload):
        if isinstance(payload, str):
            return KeyEventSchema.model_validate_json(payload)
        return KeyEventSchema.model_validate(payload)
