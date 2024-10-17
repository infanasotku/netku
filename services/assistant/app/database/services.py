from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, Optional

from database.models import User
from database.orm import AbstractRepository, Repository
from database.schemas import UserSchema


class ServiceFactory:
    """Specifies factory for DB services."""

    def __init__(self, get_db: Callable):
        self.get_db = get_db

    @asynccontextmanager
    async def user_service_factory(self) -> AsyncGenerator["UserService", None]:
        async with self.get_db() as session:
            yield UserService(Repository(session))


class UserService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    async def get_user_by_telegram_id(self, id: int) -> Optional[UserSchema]:
        """Returns user by `UserSchema.telegram_id`.
        - Returns `UserSchema` if it exist in db, `None` otherwise."""
        return await self.repository.find_first(UserSchema, User, User.telegram_id, id)

    async def get_users(self) -> list[UserSchema]:
        """Returns all user in db."""
        return await self.repository.get_all(UserSchema, User)
