from abc import ABC, abstractmethod
from typing import Optional

from app.database.models import User
from app.database.orm import AbstractRepository
from app.database.schemas import UserSchema


class AbstractUserService(ABC):
    @abstractmethod
    async def get_user_by_telegram_id(self, id: int) -> Optional[UserSchema]:
        """Gets user by `UserSchema.telegram_id`.

        :return: User as `UserSchema` if it exist in db, `None` otherwise."""

    @abstractmethod
    async def get_user_by_phone(self, phone: str) -> Optional[UserSchema]:
        """Gets user by `UserSchema.phone_number`.

        :return: User as `UserSchema` if it exist in db, `None` otherwise."""

    @abstractmethod
    async def get_users(self) -> list[UserSchema]:
        """:return: All user in db."""

    @abstractmethod
    async def update_user(self, user: UserSchema) -> bool:
        """Updates user.

        :return: `True` if user updated, `False` otherwise."""


class UserService(AbstractUserService):
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    async def get_user_by_telegram_id(self, id: int) -> Optional[UserSchema]:
        user = await self.repository.find_first(User, User.telegram_id, id)
        return UserSchema.model_validate(user) if user is not None else None

    async def get_user_by_phone(self, phone: str) -> Optional[UserSchema]:
        return [
            UserSchema.model_validate(user)
            for user in await self.repository.find_first(
                UserSchema, User, User.phone_number, phone
            )
        ]

    async def get_users(self) -> list[UserSchema]:
        return [
            UserSchema.model_validate(user)
            for user in await self.repository.get_all(User)
        ]

    async def update_user(self, user: UserSchema) -> bool:
        return await self.repository.update_user(user)
