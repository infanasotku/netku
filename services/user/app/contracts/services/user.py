from abc import abstractmethod
from collections.abc import Iterable

from app.contracts.services.base import BaseService
from app.schemas.user import UserSchema, UserUpdateSchema


class UserService(BaseService):
    @abstractmethod
    async def get_users_by_id(self, ids: Iterable[int]) -> list[UserSchema]:
        """:return: users by their `UserSchema.id`."""

    async def get_user_by_id(self, id: int) -> UserSchema | None:
        """Gets user by `UserSchema.id`.

        :return: User as `UserSchema` if it exist in db, `None` otherwise."""
        users = await self.get_users_by_id((id,))

        return users[0] if len(users) > 0 else None

    @abstractmethod
    async def get_user_by_telegram_id(self, id: int) -> UserSchema | None:
        """Gets user by `UserSchema.telegram_id`.

        :return: User as `UserSchema` if it exist in db, `None` otherwise."""

    @abstractmethod
    async def get_user_by_phone(self, phone: str) -> UserSchema | None:
        """Gets user by `UserSchema.phone_number`.

        :return: User as `UserSchema` if it exist in db, `None` otherwise."""

    @abstractmethod
    async def get_users(self) -> list[UserSchema]:
        """:return: All users in db."""

    @abstractmethod
    async def update_user(
        self, user_id: int, user_update: UserUpdateSchema
    ) -> UserSchema:
        """Updates user.

        :return: `True` if user updated, `False` otherwise."""
