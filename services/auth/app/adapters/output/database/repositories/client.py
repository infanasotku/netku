from sqlalchemy import select

from common.sql.repository import SQLBaseRepository

from app.contracts.repositories import ClientRepository
from app.schemas.client import ClientSchema
from app.infra.database.models import Client

from app.adapters.output.database import converters


class SQLClientRepository(ClientRepository, SQLBaseRepository):
    async def get_client_by_client_id(self, client_id: int) -> ClientSchema | None:
        s = select(Client).filter(Client.client_id == client_id)

        client = (await self._session.execute(s)).scalars().first()
        if client is None:
            return None

        return converters.client_to_client_schema(client)
