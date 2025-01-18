from common.contracts.services import AuthService
from common.contracts.clients import SecurityClient


class LocalAuthService(AuthService):
    def __init__(
        self,
        security_client: SecurityClient,
    ):
        self.security_client = security_client

    async def introspect(self, token):
        return self.security_client.parse_access_token(token)
