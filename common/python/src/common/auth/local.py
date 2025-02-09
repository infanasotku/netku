from common.contracts.services import AuthService
from common.contracts.clients import SecurityClient, MessageInClient
from common.schemas.client_credential import ClientCredentials


class LocalAuthService(AuthService):
    def __init__(
        self, security_client: SecurityClient, message_client: MessageInClient | None
    ):
        """
        Args:
            message_client: Client for receiving scopes updates.
        """
        self.security_client = security_client
        if message_client is not None:
            message_client.register(self._process_update)

    async def _process_update(self, msg: str):
        """Processes scopes updates."""
        creds = ClientCredentials.model_validate_json(msg)
        print("Credentials", creds)

    async def introspect(self, token):
        return self.security_client.parse_access_token(token)
