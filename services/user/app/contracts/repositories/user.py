from abc import abstractmethod
from collections.abc import Iterable

from common.contracts.repository import BaseRepository

from app.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema


class UserRepository(BaseRepository):
    @abstractmethod
    async def get_users_by_id(self, ids: Iterable[int]) -> list[UserSchema]:
        """:return: users by their `UserSchema.id`."""

    async def get_user_by_id(self, id: int) -> UserSchema | None:
        """Gets user by `UserSchema.id`.

        :return: User as `UserSchema` if it exist in db, `None` otherwise."""
        users = await self.get_users_by_id((id,))

        return users[0] if len(users) > 0 else None

    @abstractmethod
    async def get_user_by_telegram_id(self, telegram_id: int) -> UserSchema | None:
        """Gets user by `telegram_id`.

        :return: User if it exist in DB, `None` otherwise."""

    @abstractmethod
    async def get_user_by_phone(self, phone_number: str) -> UserSchema | None:
        """Gets user by `phone_number`.

        :return: User if it exist in DB, `None` otherwise."""

    @abstractmethod
    async def get_all_users(self) -> tuple[UserSchema]:
        """Gets all users from DB."""

    @abstractmethod
    async def create_user(self, user_create: UserCreateSchema) -> UserSchema:
        """Creates user in DB.

        :return: Created user.
        """

    @abstractmethod
    async def update_user(
        self, user_id: int, user_update: UserUpdateSchema
    ) -> UserSchema:
        """Update user in DB.

        :return: Updated user.
        """
