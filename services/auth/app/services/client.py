from common.contracts.clients import SecurityClient
from common.events.scope import ScopeChangedEvent
from common.schemas.client_credential import ClientCredentials

from app.contracts.uow import ClientScopeUnitOfWork
from app.contracts.services import ClientService
from app.schemas.client import ClientFullSchema
from app.schemas.token import TokenSchema


class ClientServiceImpl(ClientService):
    token_type = "bearer"

    def __init__(
        self,
        cs_uow: ClientScopeUnitOfWork,
        security_client: SecurityClient,
        scope_event: ScopeChangedEvent,
    ):
        self._security_client = security_client
        self._scope_event = scope_event
        self._cs_uow = cs_uow

    async def get_client_with_scopes_by_external_client_id(self, external_client_id):
        async with self._cs_uow as uow:
            client = await uow.client.get_client_by_external_client_id(
                external_client_id
            )
            if client is None:
                return

            scopes = await uow.client_scope.get_scopes_by_client_id(client.id)

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
        if not self._security_client.verify_source(
            client_secret, client.hashed_client_secret
        ):
            return

        access_token = self._security_client.create_access_token(
            {"sub": external_client_id, "scopes": " ".join(client.scopes)}
        )
        return TokenSchema(access_token=access_token, token_type=self.token_type)

    async def introspect(self, token):
        return self._security_client.parse_access_token(token)

    async def remove_client_scope(self, client_scope_id):
        async with self._cs_uow as uow:
            client_id = await uow.client_scope.get_client_id_by_client_scope_id(
                client_scope_id
            )
            client_external_id = await uow.client.get_client_external_id_by_id(
                client_id
            )
            scopes = await uow.client_scope.remove_client_scope(client_scope_id)
            creds = ClientCredentials(
                external_client_id=client_external_id, scopes=scopes
            )
            await self._scope_event.send(creds)

            return scopes

    async def create_client_scope(self, client_id, scope_id):
        async with self._cs_uow as uow:
            scopes = await uow.client_scope.create_client_scope(client_id, scope_id)
            client_external_id = await uow.client.get_client_external_id_by_id(
                client_id
            )
            creds = ClientCredentials(
                external_client_id=client_external_id, scopes=scopes
            )
            await self._scope_event.send(creds)

            return scopes
