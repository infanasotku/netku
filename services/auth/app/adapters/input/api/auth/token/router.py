from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, Security, status, Depends
from dependency_injector.wiring import Provide, inject

from app.container import Container
from common.schemas.client_credential import ClientCredentials
from app.contracts.services import ClientService
from app.schemas.token import TokenPayload, TokenSchema

from app.adapters.input.api.dependencies import Authorization


router = APIRouter()


@router.post("/")
@inject
async def create_token(
    client_id: Annotated[str, Body(examples=["johndoe"])],
    client_secret: Annotated[str, Body(examples=["johndoe_secret"])],
    client_service: ClientService = Depends(Provide[Container.client_service]),
) -> TokenSchema:
    """Creates token for specified `client_id` and `client_secret`.

    Returns:
        Token with type if client authenticated.

    Raises:
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED):
            If error occured with client credentials.
    """
    token = await client_service.authenticate(client_id, client_secret)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.post("/introspect")
@inject
async def introspect_token(
    token: str = Body(examples=["jwt.token.example"]),
    client_service: ClientService = Depends(Provide[Container.client_service]),
    _: ClientCredentials = Security(
        Authorization,
        scopes=["auth:read"],
    ),
) -> TokenPayload | None:
    """Introspects `token`.

    Returns:
        Token payload with token introspection
        if client authenticated, `null` otherwise.
    """
    return await client_service.introspect(token)
