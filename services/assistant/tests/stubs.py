from typing import Any
from app.database.orm import AbstractRepository, ModelT
from app.database.models import XrayRecord


class StubRepository(AbstractRepository):
    async def find_first(
        self, model: type[ModelT], column: Any, value: Any
    ) -> ModelT | None:
        raise NotImplementedError

    async def get_all(self, model: type[ModelT]) -> list[ModelT]:
        raise NotImplementedError

    async def create(self, entity: ModelT) -> ModelT:
        raise NotImplementedError

    async def update(self, entity: ModelT) -> None:
        raise NotImplementedError

    async def get_xray_record(self) -> XrayRecord | None:
        raise NotImplementedError
