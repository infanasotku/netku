from app.contracts.repositories import UserRepository
from app.contracts.services import UserService
from app.contracts.clients import NotificationClient

from app.schemas.user import UserSchema, UserUpdateSchema


class UserServiceImpl(UserService):
    def __init__(
        self, user_repository: UserRepository, notification_client: NotificationClient
    ):
        self._user_repository = user_repository
        self._notification_client = notification_client

    async def get_user_by_telegram_id(self, id: int) -> UserSchema | None:
        return await self._user_repository.get_user_by_telegram_id(id)

    async def get_user_by_phone(self, phone: str) -> UserSchema | None:
        return await self._user_repository.get_user_by_phone(phone)

    async def get_users(self) -> list[UserSchema]:
        return await self._user_repository.get_all_users()

    async def update_user(self, user_id, user_update: UserUpdateSchema) -> UserSchema:
        return await self._user_repository.update_user(user_id, user_update)

    async def get_users_by_active_subscriptions(
        self, subscriptions: list[str], every: bool = False
    ) -> list[UserSchema]:
        return await self._user_repository.get_users_by_active_subscriptions(
            subscriptions, every
        )

    async def send_notify_by_subscriptions(
        self, subscriptions: list[str], message: str
    ) -> None:
        users = await self.get_users_by_active_subscriptions(subscriptions, True)

        for user in users:
            if user.telegram_id is not None:
                await self._notification_client.send_message(message, user)
