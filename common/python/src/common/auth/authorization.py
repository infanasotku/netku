from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes

from common.contracts.services import AuthService
from common.schemas.client_credential import ClientCredentials


class Authorization:
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    async def __call__(
        self,
        scopes: SecurityScopes,
        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
    ) -> ClientCredentials:
        """Checks `credentials` for `scopes`.

        Raises:
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED):
                If credential is invalid.

        Returns:
            Client credential with client **id** and client **scopes**
            if client authorization successful.
        """
        token = credentials.credentials
        scheme = credentials.scheme

        if scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect scheme of token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        client_credential = await self._auth_service.authorize(token, scopes.scopes)

        if client_credential is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return client_credential
