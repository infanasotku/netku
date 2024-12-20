from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase


class MongoDBConnection:
    def __init__(self, mongo_dsn: str, default_db_name: str | None = None):
        """
        :param default_db_name: if defined `MongoDBConnection.get_db`
        might use without explicit `db_name`.
        """
        self._client = AsyncMongoClient(mongo_dsn)
        self._default_db_name = default_db_name

    def get_db(self, db_name: str | None = None) -> AsyncDatabase:
        if db_name is None:
            db_name = self._default_db_name

            if db_name is None:
                raise Exception("Params db_name and default_database_name are None")

        return self._client[db_name]
