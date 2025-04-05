from datetime import datetime
import pytz
import aiohttp
import aiohttp.client_exceptions

from common.schemas.token import (
    TokenPayload,
    TokenPayloadShort,
)
from common.contracts.services import AuthService
from common.http.retry import retry
import common


class _AuthClient:
    def __init__(self, auth_url: str, *, with_ssl: bool = True):
        self._auth_url = auth_url
        self._with_ssl = with_ssl

    @retry
    async def introspect_token(
        self, token: str, *, access_token: str
    ) -> TokenPayload | None:
        """Sends request for introspect token to auth service.

        Returns:
            Token payload if introspection successful, `None` otherwise.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._auth_url}/api/auth/token/introspect",
                data=token,
                headers={"Authorization": f"Bearer {access_token}"},
                ssl=self._with_ssl,
            ) as resp:
                if resp.status != 200:
                    return
                body = await resp.text()
                if body == "null":
                    return
                return TokenPayload.model_validate_json(body)

    @retry
    async def create_token(
        self, external_client_id: str, client_secret: str
    ) -> str | None:
        """Sends request for create token to auth service.

        Returns:
            Token if token created, `None` otherwise.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._auth_url}/api/auth/token/",
                json={
                    "external_client_id": external_client_id,
                    "client_secret": client_secret,
                },
                ssl=self._with_ssl,
            ) as resp:
                if resp.status != 200:
                    return
                body: dict = await resp.json()
                return body.get("access_token")


class RemoteAuthService(AuthService):
    def __init__(
        self,
        auth_url: str,
        *,
        cliend_id: str,
        client_secret: str,
        with_ssl: bool = True,
    ):
        self._cliend_id = cliend_id
        self._client_secret = client_secret
        self._token_payload: TokenPayloadShort | None = None
        self._auth_client = _AuthClient(auth_url, with_ssl=with_ssl)

    def _compare_time(self, first: datetime, second: datetime) -> bool:
        utc = pytz.UTC
        first = first.replace(tzinfo=utc)
        second = second.replace(tzinfo=utc)

        return first < second

    def _check_token(self) -> bool:
        """Checks token for expiration.

        Returns:
            `True` if token valid, `False` otherwise.
        """
        if self._token_payload is None:
            return False

        now = common.now()

        return self._compare_time(now, self._token_payload.expire)

    async def _update_token(self) -> bool:
        """Updates token.

        Returns:
            `True` if token updated successful, `False` otherwise.
        """
        token = await self._auth_client.create_token(
            self._cliend_id, self._client_secret
        )
        if token is None:
            return False

        payload = await self._auth_client.introspect_token(token, access_token=token)
        if payload is None:
            return False

        self._token_payload = TokenPayloadShort(token=token, expire=payload.expire)
        return True

    async def introspect(self, token):
        if not self._check_token() and not await self._update_token():
            return

        return await self._auth_client.introspect_token(
            token, access_token=self._token_payload.token
        )
