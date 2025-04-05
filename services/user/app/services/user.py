from app.contracts.uow import UserUnitOfWork
from app.contracts.services import UserService

from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema


class UserServiceImpl(UserService):
    def __init__(self, u_uow: UserUnitOfWork):
        self._u_uow = u_uow

    async def get_users_by_id(self, ids):
        async with self._u_uow as uow:
            return await uow.user.get_users_by_id(ids)

    async def get_user_by_telegram_id(self, id: int) -> UserSchema | None:
        async with self._u_uow as uow:
            return await uow.user.get_user_by_telegram_id(id)

    async def get_user_by_phone(self, phone: str) -> UserSchema | None:
        async with self._u_uow as uow:
            return await uow.user.get_user_by_phone(phone)

    async def get_users(self) -> list[UserSchema]:
        async with self._u_uow as uow:
            return await uow.user.get_all_users()

    async def update_user(self, user_id, user_update: UserUpdateSchema) -> UserSchema:
        async with self._u_uow as uow:
            return await uow.user.update_user(user_id, user_update)

    async def create_user(self, user_create: UserCreateSchema) -> UserSchema:
        async with self._u_uow as uow:
            return await uow.user.create_user(user_create)
