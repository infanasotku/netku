import asyncio
from typing import Union
from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ErrorEvent,
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from bot.states import BaseState, BookingAccountAdding
import bot.utils as utils
import bot.text as text
import bot.kb as kb

from settings import logger
from xray import xray


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


# region Services


# region Proxy
@router.message(Command("proxy"))
async def subscribe_for_proxy(message: Message):
    user = utils.get_user(message)

    if not user:
        await message.answer(text.please_click_start)
        return

    if user.proxy_subscription:
        await message.answer("You already subscribeted to proxy!")
        return

    utils.subscribe_user(user, "proxy")
    await message.answer("You subscribeted to proxy!")


@router.message(Command("proxy_uid"))
async def get_proxy_uuid(message: Message):
    user = utils.get_user(message)

    if not user:
        await message.answer(text.please_click_start)
        return

    if not user.proxy_subscription:
        await message.answer("You didn't subscribe to proxy!")
        return

    return await message.answer(hbold(xray.uid))


# endregion


# region Booking
@router.callback_query(F.data == "get_booking_menu")
@router.message(Command("machine_booking"))
async def get_booking_menu(message: Union[Message, CallbackQuery]):
    if isinstance(message, CallbackQuery):
        message = message.message

    user = utils.get_user(message)

    if not user:
        await message.answer(text.please_click_start)
        return

    await utils.try_edit_or_answer(
        message,
        f"Now booked: {utils.get_booking_machine_count(message)}",
        kb.booking_menu,
    )


@router.callback_query(F.data == "create_booking_account_menu")
async def get_booking_account_creating_menu(callback: CallbackQuery, state: FSMContext):
    await utils.try_edit_or_answer(
        callback.message,
        text.create_booking_account_text,
        await kb.generate_booking_account_creating_menu(state),
    )


# Fill
@router.callback_query(F.data == "submit_booking_account")
async def submit_booking_account(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    email = data["email"]
    password = data["password"]
    # TODO: Email validation


@router.callback_query(F.data == "fill_booking_email")
async def fill_booking_email(callback: CallbackQuery, state: FSMContext):
    await utils.fill_field(
        callback.message,
        state,
        "email",
        kb.booking_account_creating_button,
        BookingAccountAdding.email,
    )


@router.message(BookingAccountAdding.email)
async def apply_booking_email(message: Message, state: FSMContext):
    await utils.apply_field(
        message,
        state,
        "email",
        text.create_booking_account_text,
        kb.generate_booking_account_creating_menu,
    )


@router.callback_query(F.data == "fill_booking_password")
async def fill_booking_password(callback: CallbackQuery, state: FSMContext):
    await utils.fill_field(
        callback.message,
        state,
        "password",
        kb.booking_account_creating_button,
        BookingAccountAdding.password,
    )


@router.message(BookingAccountAdding.password)
async def apply_booking_password(message: Message, state: FSMContext):
    await utils.apply_field(
        message,
        state,
        "password",
        text.create_booking_account_text,
        kb.generate_booking_account_creating_menu,
    )


# endregion
# endregion


# region Common
@router.callback_query(F.data == "hide_keyboard")
async def hide_keyboard(callback: CallbackQuery):
    if not await utils.try_delete_message(callback.message):
        await callback.message.answer("Keyboard too old")


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


# endregion
