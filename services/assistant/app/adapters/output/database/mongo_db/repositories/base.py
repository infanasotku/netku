from pymongo.asynchronous.collection import AsyncCollection

from app.contracts.repositories.base import BaseRepository


class MongoBaseRepository(BaseRepository):
    collection_name: str = "base_collection"

    def __init__(self, collection: AsyncCollection):
        if collection.name != self.collection_name:
            raise Exception(
                f"Collection {collection.name} is not {self.collection_name}."
            )

        self._collection = collection
