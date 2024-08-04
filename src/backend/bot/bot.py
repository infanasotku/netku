import logging
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import settings


dispatcher = Dispatcher()
bot = Bot(
    token=settings.get().bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
logger = logging.getLogger("uvicorn.error")
