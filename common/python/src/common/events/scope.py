from common.contracts.event import BaseEvent
from common.schemas.client_credential import ClientCredentials


class ScopeChangedEvent(BaseEvent[ClientCredentials]):
    name = "scopes.changed"

    @staticmethod
    def _dumps(data):
        return data.model_dump_json()

    @staticmethod
    def _loads(payload):
        if isinstance(payload, str):
            return ClientCredentials.model_validate_json(payload)
        return ClientCredentials.model_validate(payload)
