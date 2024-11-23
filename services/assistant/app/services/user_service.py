from app.contracts.repositories import UserRepository
from app.contracts.services import UserService

from app.schemas.user_schemas import UserSchema, UserUpdateSchema


class UserServiceImpl(UserService):
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
