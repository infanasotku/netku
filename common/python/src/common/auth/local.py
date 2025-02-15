from common.contracts.services import AuthService
from common.contracts.clients import SecurityClient
from common.schemas.client_credential import ClientCredentials


class LocalAuthService(AuthService):
    def __init__(self, security_client: SecurityClient):
        self.security_client = security_client

    async def process_update(self, credentials: ClientCredentials):
        """Processes scopes updates."""
        print("Credentials", credentials)

    async def introspect(self, token):
        return self.security_client.parse_access_token(token)
