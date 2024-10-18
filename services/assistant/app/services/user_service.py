from typing import Optional

from database.models import User
from database.orm import AbstractRepository
from database.schemas import UserSchema


class UserService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    async def get_user_by_telegram_id(self, id: int) -> Optional[UserSchema]:
        """Gets user by `UserSchema.telegram_id`.
        - Returns user as `UserSchema` if it exist in db, `None` otherwise."""
        user = await self.repository.find_first(User, User.telegram_id, id)
        return UserSchema.model_validate(user) if user is not None else None

    async def get_user_by_phone(self, phone: str) -> Optional[UserSchema]:
        """Gets user by `UserSchema.phone_number`.
        - Returns user as `UserSchema` if it exist in db, `None` otherwise."""
        return [
            UserSchema.model_validate(user)
            for user in await self.repository.find_first(
                UserSchema, User, User.phone_number, phone
            )
        ]

    async def get_users(self) -> list[UserSchema]:
        """Returns all user in db."""
        return [
            UserSchema.model_validate(user)
            for user in await self.repository.get_all(User)
        ]

    async def update_user(self, user: UserSchema) -> bool:
        """Updates user.
        - Returns `True` if user updated, `False` otherwise."""

        return await self.repository.update_user(user)
