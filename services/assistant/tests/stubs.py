from typing import Any, Type
from app.database.orm import AbstractRepository, ModelT
from app.database.models import XrayRecord

from app.schemas.user_schemas import UserSchema


class StubRepository(AbstractRepository):
    async def find_first(
        self, model: Type[ModelT], column: Any, value: Any
    ) -> ModelT | None:
        raise NotImplementedError

    async def get_all(self, model: Type[ModelT]) -> list[ModelT]:
        raise NotImplementedError

    async def update_user(self, user: UserSchema) -> bool:
        raise NotImplementedError

    async def create_booking_account(
        self, user: UserSchema, email: str, password: str
    ) -> bool:
        raise NotImplementedError

    async def update_xray_record(self, uid: str) -> None:
        raise NotImplementedError

    async def get_xray_record(self) -> XrayRecord | None:
        raise NotImplementedError
