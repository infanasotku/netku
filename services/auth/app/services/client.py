from common.contracts.clients import SecurityClient

from app.contracts.repositories import ClientScopeRepository, ClientRepository
from app.contracts.services import ClientService

from app.schemas.client import ClientFullSchema
from app.schemas.token import TokenSchema


class ClientServiceImpl(ClientService):
    token_type = "bearer"

    def __init__(
        self,
        security_client: SecurityClient,
        client_scope_repo: ClientScopeRepository,
        client_repo: ClientRepository,
    ):
        self.security_client = security_client
        self.client_scope_repo = client_scope_repo
        self.client_repo = client_repo

    async def get_client_with_scopes_by_client_id(self, client_id):
        client = await self.client_repo.get_client_by_client_id(client_id)
        if client is None:
            return

        scopes = await self.client_scope_repo.get_scopes_by_client_id(client.id)

        return ClientFullSchema(
            id=client.id,
            client_id=client.client_id,
            hashed_client_secret=client.hashed_client_secret,
            scopes=scopes,
        )

    async def authenticate(self, client_id, client_secret):
        client = await self.get_client_with_scopes_by_client_id(client_id)
        if client is None:
            return
        if not self.security_client.verify_source(
            client_secret, client.hashed_client_secret
        ):
            return

        access_token = self.security_client.create_access_token(
            {"sub": client_id, "scopes": " ".join(client.scopes)}
        )
        return TokenSchema(access_token=access_token, token_type=self.token_type)

    async def introspect(self, token):
        return self.security_client.parse_access_token(token)
