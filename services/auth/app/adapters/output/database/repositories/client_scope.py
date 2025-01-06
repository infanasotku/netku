from sqlalchemy import select

from common.sql.repository import SQLBaseRepository

from app.contracts.repositories import ClientScopeRepository
from app.infra.database.models import ClientScope, Scope


class SQLClientScopeRepository(ClientScopeRepository, SQLBaseRepository):
    async def get_scopes_by_client_id(self, client_id: int) -> list[str]:
        client_scope_select = (
            select(ClientScope.id).filter(ClientScope.client_id == client_id).subquery()
        )
        s = select(Scope.name).filter(Scope.id.in_(client_scope_select))

        scopes = (await self._session.execute(s)).scalars().all()

        return list(scopes)
