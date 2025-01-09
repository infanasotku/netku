from datetime import datetime
from common.schemas import TokenPayload
from common.contracts.services import AuthService


class RemoteAuthService(AuthService):
    def __init__(self, auth_url: str, cliend_id: str, client_secret: str):
        self._auth_url = auth_url
        self._cliend_id = cliend_id
        self._client_secret = client_secret
        self._token: TokenPayload | None = None

    def check_token(self) -> bool:
        """Checks token for expiration.

        Returns:
            `True` if token valid, `False` otherwise.
        """
        if self._token is None:
            return False

        now = datetime.now()
        return self._token.expire < now

    async def update_token(self):
        pass

    async def authorize(self, token, needed_scopes):
        if not self.check_token():
            await self.update_token()
