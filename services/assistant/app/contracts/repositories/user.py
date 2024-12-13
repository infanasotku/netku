from abc import abstractmethod

from app.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema

from app.contracts.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    @abstractmethod
    async def get_user_by_id(self, id: int) -> UserSchema | None:
        """Gets user by `id`.

        :return: User if it exist in DB, `None` otherwise."""

    @abstractmethod
    async def get_user_by_telegram_id(self, telegram_id: int) -> UserSchema | None:
        """Gets user by `telegram_id`.

        :return: User if it exist in DB, `None` otherwise."""

    @abstractmethod
    async def get_user_by_phone(self, phone_number: str) -> UserSchema | None:
        """Gets user by `phone_number`.

        :return: User if it exist in DB, `None` otherwise."""

    @abstractmethod
    async def get_all_users(self) -> list[UserSchema]:
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

    @abstractmethod
    async def get_users_by_active_subscriptions(
        self, subscriptions: list[str], every: bool = False
    ) -> list[UserSchema]:
        """Finds user with active `subscriptions`.

        :param every: If `True` then matches user with all specified `subscriptions`.

        :return: Found users."""
