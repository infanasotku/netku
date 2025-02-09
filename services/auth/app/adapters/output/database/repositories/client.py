from sqlalchemy import select

from common.sql.repository import SQLBaseRepository

from app.contracts.repositories import ClientRepository
from app.schemas.client import ClientSchema
from app.infra.database.models import Client

from app.adapters.output.database import converters


class SQLClientRepository(ClientRepository, SQLBaseRepository):
    async def _get_client_by(self, column, value) -> ClientSchema | None:
        s = select(Client).filter(column == value)

        client = (await self._session.execute(s)).scalars().first()
        if client is None:
            return

        return converters.client_to_client_schema(client)

    async def get_client_by_external_client_id(
        self, external_client_id: int
    ) -> ClientSchema | None:
        return await self._get_client_by(Client.external_client_id, external_client_id)

    async def get_client_external_id_by_id(self, id):
        s = select(Client.external_client_id).filter(Client.id == id)
        return (await self._session.execute(s)).scalar_one()
