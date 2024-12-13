from contextlib import asynccontextmanager
from typing import AsyncGenerator, Type, TypeVar
from pymongo.asynchronous.collection import AsyncCollection

from app.infra.database.mongo_db.orm import GetMongoDB
from app.infra.database.mongo_db.repositories.base import MongoBaseRepository


class MongoRepositoryFactory:
    MongoRepositoryT = TypeVar("MongoRepositoryT", bound=MongoBaseRepository)

    def __init__(
        self,
        get_db: GetMongoDB,
        repository_type: Type[MongoRepositoryT],
    ):
        self.get_db = get_db
        self._Repo = repository_type
        self.collection: AsyncCollection

    # Async need for compatibility with app.contracts.protocols.CreateRepository
    @asynccontextmanager
    async def create(self) -> AsyncGenerator[MongoRepositoryT, None]:
        if self.collection is not None:
            yield self._Repo(self.collection)
        else:
            db = self.get_db()
            collection: AsyncCollection = db(self._Repo.collection_name)
            self.collection = collection
            yield self._Repo(collection)
