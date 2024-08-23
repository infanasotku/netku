import asyncio
from aiogram import Router
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ErrorEvent,
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.states import BaseState
import bot.utils as utils
import bot.text as text

from settings import logger


router = Router(name="main")


@router.message(
    Command("start"),
)
async def start(message: Message, state: FSMContext):
    user = utils.get_user(message)

    if user:
        await state.set_state(BaseState.none)
        await message.answer(f"Hello! {message.from_user.first_name}!")
    else:
        await state.set_state(BaseState.registration)
        share_phone = KeyboardButton(text="Share", request_contact=True)
        keyboard = ReplyKeyboardMarkup(keyboard=[[share_phone]])
        await message.answer(
            "Hello! For identification you need to share your phone.",
            reply_markup=keyboard,
        )


@router.message(Command("stop"))
async def stop(message: Message):
    user = utils.get_user(message)

    if not user:
        await message.answer(text.please_click_start)
        return

    utils.unsubscribe_user(user, "all")
    await message.answer("Subscriptions canceled!")


@router.message(Command("proxy"))
async def sign_up_for_proxy(message: Message):
    user = utils.get_user(message)

    if not user:
        await message.answer(text.please_click_start)
        return

    utils.subscribe_user(user, "proxy")
    await message.answer("You subscribeted to proxy!")


@router.message(BaseState.registration)
async def registrate(message: Message):
    if not message.contact:
        await utils.try_delete_message(message)
        return

    user = utils.registrate_user(message.contact)
    if user:
        await message.answer(
            "Registration successful!", reply_markup=ReplyKeyboardRemove()
        )
    if not user:
        await message.answer(
            "Sorry, you have not enough permissions for registration.",
            reply_markup=ReplyKeyboardRemove(),
        )


@router.message(BaseState.none)
async def delete_extra(message: Message):
    await utils.try_delete_message(message)


@router.error()
async def error_handler(event: ErrorEvent):
    logger.error(f"Error occurred: {event.exception}")
    message = event.update.callback_query.message
    await utils.try_delete_message(message)
    msg = await message.answer(
        "Error occurred! Contact your admin.", reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.sleep(3)
    await msg.delete()
