from collections.abc import Iterable
from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute

from common.sql.repository import SQLBaseRepository
from common.sql.orm import selectinload_all

from app.contracts.repositories import UserRepository
from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema
from app.infra.database.models import User

from app.adapters.output.database import converters


class SQLUserRepository(UserRepository, SQLBaseRepository):
    async def get_users_by_id(self, ids: Iterable[int]):
        s = select(User).options(*selectinload_all(User)).filter(User.id.in_(ids))

        users = (await self._session.execute(s)).scalars().all()

        return [converters.user_to_user_schema(user) for user in users]

    async def _get_user_model_by_column(
        self, column: InstrumentedAttribute, value
    ) -> User | None:
        s = select(User).options(*selectinload_all(User)).filter(column == value)
        return (await self._session.execute(s)).scalars().first()

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserSchema | None:
        user = await self._get_user_model_by_column(User.telegram_id, telegram_id)

        if user is None:
            return None

        return converters.user_to_user_schema(user)

    async def get_user_by_phone(self, phone_number: str) -> UserSchema | None:
        user = await self._get_user_model_by_column(User.phone_number, phone_number)

        if user is None:
            return None

        return converters.user_to_user_schema(user)

    async def get_all_users(self) -> list[UserSchema]:
        s = select(User).options(*selectinload_all(User))

        users = (await self._session.execute(s)).scalars().all()

        return [converters.user_to_user_schema(user) for user in users]

    async def create_user(self, user_create: UserCreateSchema) -> UserSchema:
        user = converters.user_create_schema_to_user(user_create)
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)

        return converters.user_to_user_schema(user)

    async def update_user(
        self, user_id: int, user_update: UserUpdateSchema
    ) -> UserSchema:
        user = await self._get_user_model_by_column(User.id, user_id)

        if user is None:
            raise Exception(f"User with id {user_id} not exist.")

        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        await self._session.flush()
        await self._session.refresh(user)

        return converters.user_to_user_schema(user)
