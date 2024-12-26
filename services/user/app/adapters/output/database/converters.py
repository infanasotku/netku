from app.schemas.user import UserCreateSchema, UserSchema
from app.infra.database.models import User


def user_create_schema_to_user(user_create: UserCreateSchema) -> User:
    return User(
        phone_number=user_create.phone_number,
        telegram_id=user_create.telegram_id,
        proxy_subscription=user_create.proxy_subscription,
        availability_subscription=user_create.availability_subscription,
    )


def user_to_user_schema(user: User) -> UserSchema:
    return UserSchema.model_validate(user)
