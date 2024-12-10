from pymongo.asynchronous.collection import AsyncCollection


class MongoBaseRepository:
    collection_name: str = "base_collection"

    def __init__(self, collection: AsyncCollection):
        if collection.name != self.collection_name:
            raise Exception(
                f"Collection {collection.name} is not {self.collection_name}."
            )

        self._collection = collection
