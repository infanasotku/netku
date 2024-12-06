from typing import Callable
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase


def get_db_factory(
    mongo_dsn: str, default_db_name: str | None = None
) -> Callable[[str], AsyncDatabase]:
    """Returns method which returns mongo database database name.

    :param default_db_name: if defined `get_db` might use without explicit `db_name`.
    """
    client = AsyncMongoClient(mongo_dsn)

    def get_db(db_name: str | None = None) -> AsyncDatabase:
        if db_name is None:
            db_name = default_db_name

            if db_name is None:
                raise Exception("Params db_name and default_database_name are None")

        return client[db_name]

    return get_db
