from sqlalchemy import select

from common.sql.repository import SQLBaseRepository

from app.contracts.repositories import ClientScopeRepository
from app.infra.database.models import ClientScope, Scope


class SQLClientScopeRepository(ClientScopeRepository, SQLBaseRepository):
    async def get_scopes_by_client_id(self, id: int) -> list[str]:
        client_scope_select = select(ClientScope.scope_id).filter(
            ClientScope.client_id == id
        )
        s = select(Scope.name).filter(Scope.id.in_(client_scope_select))

        scopes = (await self._session.execute(s)).scalars().all()

        return list(scopes)

    async def get_client_id_by_client_scope_id(self, client_scope_id):
        s = select(ClientScope.client_id).filter(ClientScope.id == client_scope_id)
        return (await self._session.execute(s)).scalar_one()

    async def remove_client_scope(self, client_scope_id):
        s = select(ClientScope).filter(ClientScope.id == client_scope_id)
        client_scope = (await self._session.execute(s)).scalars().first()

        if client_scope is None:
            raise ValueError(f"Client scope with id: {client_scope_id} not exist.")

        client_id = client_scope.client_id
        await self._session.delete(client_scope)

        return await self.get_scopes_by_client_id(client_id)
