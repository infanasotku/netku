from abc import ABC, abstractmethod

from app.schemas.user_schemas import UserSchema, UserCreateSchema, UserUpdateSchema


class UserRepository(ABC):
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
