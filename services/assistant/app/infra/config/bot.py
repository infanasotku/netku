import uuid
from pydantic_settings import BaseSettings
from pydantic import Field


class BotSettings(BaseSettings):
    bot_token: str = Field(validation_alias="BOT_TOKEN")
    telegram_token: str = Field(
        validation_alias="TELEGRAM_TOKEN", default=str(uuid.uuid4())
    )
    bot_webhook_url: str = Field(validation_alias="BOT_WEBHOOK_URL")
