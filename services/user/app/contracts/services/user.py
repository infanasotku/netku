from abc import abstractmethod
from collections.abc import Iterable

from common.contracts.services import BaseService

from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema


class UserService(BaseService):
    @abstractmethod
    async def get_users_by_id(self, ids: Iterable[int]) -> list[UserSchema]:
        """
        Returns:
            Users by their `UserSchema.id`."""

    async def get_user_by_id(self, id: int) -> UserSchema | None:
        """Gets user by `UserSchema.id`.

        Returns:
            User as `UserSchema` if it exist in db, `None` otherwise."""
        users = await self.get_users_by_id((id,))

        return users[0] if len(users) > 0 else None

    @abstractmethod
    async def get_user_by_telegram_id(self, id: int) -> UserSchema | None:
        """Gets user by `UserSchema.telegram_id`.

        Returns:
            User as `UserSchema` if it exist in db, `None` otherwise."""

    @abstractmethod
    async def get_user_by_phone(self, phone: str) -> UserSchema | None:
        """Gets user by `UserSchema.phone_number`.

        Returns:
            User as `UserSchema` if it exist in db, `None` otherwise."""

    @abstractmethod
    async def get_users(self) -> list[UserSchema]:
        """:return: All users in db."""

    @abstractmethod
    async def create_user(self, user_create: UserCreateSchema) -> UserSchema:
        """Creates user.

        Returns:
            Created user."""

    @abstractmethod
    async def update_user(
        self, user_id: int, user_update: UserUpdateSchema
    ) -> UserSchema:
        """Updates user.

        Returns:
            Updated user."""
