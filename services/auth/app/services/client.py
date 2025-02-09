import json

from common.contracts.clients import SecurityClient

from app.contracts.repositories import ClientScopeRepository, ClientRepository
from app.contracts.services import ClientService
from common.contracts.clients import MessageOutClient

from app.schemas.client import ClientFullSchema
from app.schemas.token import TokenSchema


class ClientServiceImpl(ClientService):
    token_type = "bearer"

    def __init__(
        self,
        security_client: SecurityClient,
        client_scope_repo: ClientScopeRepository,
        client_repo: ClientRepository,
        message_out_client: MessageOutClient,
    ):
        self.security_client = security_client
        self.client_scope_repo = client_scope_repo
        self.client_repo = client_repo
        self.message_out_client = message_out_client

    async def get_client_with_scopes_by_external_client_id(self, external_client_id):
        client = await self.client_repo.get_client_by_external_client_id(
            external_client_id
        )
        if client is None:
            return

        scopes = await self.client_scope_repo.get_scopes_by_client_id(client.id)

        return ClientFullSchema(
            id=client.id,
            external_client_id=client.external_client_id,
            hashed_client_secret=client.hashed_client_secret,
            scopes=scopes,
        )

    async def authenticate(self, external_client_id, client_secret):
        client = await self.get_client_with_scopes_by_external_client_id(
            external_client_id
        )
        if client is None:
            return
        if not self.security_client.verify_source(
            client_secret, client.hashed_client_secret
        ):
            return

        access_token = self.security_client.create_access_token(
            {"sub": external_client_id, "scopes": " ".join(client.scopes)}
        )
        return TokenSchema(access_token=access_token, token_type=self.token_type)

    async def introspect(self, token):
        return self.security_client.parse_access_token(token)

    async def remove_client_scope(self, client_scope_id):
        client_id = await self.client_scope_repo.get_client_id_by_client_scope_id(
            client_scope_id
        )
        scopes = await self.client_scope_repo.remove_client_scope(client_scope_id)
        data = {"client_id": client_id, "scopes": scopes}

        await self.message_out_client.send(json.dumps(data))
        return scopes

    async def create_client_scope(self, client_id, scope_id):
        scopes = await self.client_scope_repo.create_client_scope(client_id, scope_id)
        data = {"client_id": client_id, "scopes": scopes}

        await self.message_out_client.send(json.dumps(data))
        return scopes
