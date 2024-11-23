from abc import ABC, abstractmethod

from app.repositories import UserRepository

from app.schemas.user_schemas import UserSchema, UserUpdateSchema


class AbstractUserService(ABC):
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
        """:return: All user in db."""

    @abstractmethod
    async def update_user(
        self, user_id: int, user_update: UserUpdateSchema
    ) -> UserSchema:
        """Updates user.

        :return: `True` if user updated, `False` otherwise."""


class UserService(AbstractUserService):
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def get_user_by_telegram_id(self, id: int) -> UserSchema | None:
        return await self._user_repository.get_user_by_telegram_id(id)

    async def get_user_by_phone(self, phone: str) -> UserSchema | None:
        return await self._user_repository.get_user_by_phone(phone)

    async def get_users(self) -> list[UserSchema]:
        return await self._user_repository.get_all_users()

    async def update_user(self, user_id, user_update: UserUpdateSchema) -> UserSchema:
        return await self._user_repository.update_user(user_id, user_update)
