from typing import Any, Type
from app.database.orm import AbstractRepository
from app.database.database import Base
from app.database.models import XrayRecord
from app.database.schemas import UserSchema


class StubRepository(AbstractRepository):
    async def find_first(
        self, model: Type[Base], column: Any, value: Any
    ) -> Base | None:
        raise NotImplementedError

    async def get_all(self, model: Type[Base]) -> list[Base]:
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
