from abc import abstractmethod

from app.schemas.user import UserSchema, UserUpdateSchema

from app.contracts.services.base import BaseService


class UserService(BaseService):
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

    @abstractmethod
    async def get_users_by_active_subscriptions(
        self, subscriptions: list[str], every: bool = False
    ) -> list[UserSchema]:
        """Finds user with active `subscriptions`.

        :param every: If `True` then matches user with all specified `subscriptions`.

        :return: Found users."""

    @abstractmethod
    async def send_notify_by_subscriptions(
        self, subscriptions: list[str], message: str, highlight_sep: str = "/"
    ) -> None:
        """Sends `message` to all users with active `subscriptions`.

        :param highlight_sep: message between separator will be highlighted."""
