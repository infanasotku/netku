from typing import Protocol, Type, TypeVar
from pymongo.asynchronous.database import AsyncDatabase

from app.schemas import BaseSchema


class GetMongoDB(Protocol):
    def __call__(self, db_name: str | None = ...) -> AsyncDatabase: ...


SchemaT = TypeVar("SchemaT", bound=BaseSchema)


def result_to_schema(result: dict, schema: Type[SchemaT]) -> SchemaT:
    return schema.model_validate(result)
