from fastapi import Depends
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes
from dependency_injector.wiring import Provide, inject

from common import auth
from common.schemas import ClientCredentials
from app.contracts.services.client import ClientService
from app.container import Container


@inject
async def Authorization(
    scopes: SecurityScopes,
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
    client_service: ClientService = Depends(Provide[Container.client_service]),
) -> ClientCredentials:
    return await auth.Authorization(client_service)(scopes, credentials)
