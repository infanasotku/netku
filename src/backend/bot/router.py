from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router(name="main")


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Subscription completed!")


@router.message(Command("stop"))
async def stop(message: Message):
    await message.answer("Subscription canceled!")
