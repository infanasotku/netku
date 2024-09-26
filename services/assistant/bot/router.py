import asyncio
import re
from typing import Union
from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    ErrorEvent,
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from bot.states import BaseState, BookingAccountAdding
import bot.utils as utils
import bot.text as text
import bot.kb as kb
from bot.schemas import BookingCallbackData, BookingAction

from settings import logger
from xray import xray
from db import service
from booking import booking


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
        return await message.answer(text.please_click_start)

    utils.unsubscribe_user(user, "all")
    await message.answer("Subscriptions canceled!")


@router.message(BaseState.registration)
async def registrate(message: Message):
    if not message.contact:
        return await utils.try_delete_message(message)

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
        return await message.answer(text.please_click_start)

    if user.proxy_subscription:
        return await message.answer("You already subscribeted to proxy!")

    utils.subscribe_user(user, "proxy")
    await message.answer("You subscribeted to proxy!")


@router.message(Command("proxy_uid"))
async def get_proxy_uuid(message: Message):
    user = utils.get_user(message)

    if not user:
        return await message.answer(text.please_click_start)

    if not user.proxy_subscription:
        return await message.answer("You didn't subscribe to proxy!")

    if not xray.uid:
        return await message.answer(hbold("Proxy inactive"))

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
        return await message.answer(text.please_click_start)

    await utils.try_edit_or_answer(
        message,
        f"Now booked: {await utils.get_booking_machine_count(message)}",
        kb.booking_menu,
    )


@router.callback_query(F.data == "create_booking_account_menu")
async def get_booking_account_creating_menu(callback: CallbackQuery, state: FSMContext):
    await utils.try_edit_or_answer(
        callback.message,
        text.create_booking_account_text,
        await kb.generate_booking_account_creating_menu(state),
    )


@router.callback_query(F.data == "get_booking_accounts")
async def get_booking_accounts(callback: CallbackQuery):
    user = utils.get_user(callback.message)

    accounts = user.booking_accounts

    if len(accounts) == 0:
        return await callback.answer("You haven't accounts")

    statuses = [await booking.booked(acc.email, acc.password) for acc in accounts]

    keyboard = kb.create_inline_keyboard(
        *(
            [
                InlineKeyboardButton(text=account.email, callback_data="stub"),
                InlineKeyboardButton(
                    text="Run" if not status else "Stop",
                    callback_data=BookingCallbackData(
                        user_id=user.id,
                        account_id=account.id,
                        action=BookingAction.run if not status else BookingAction.stop,
                    ).pack(),
                ),
            ]
            for account, status in zip(accounts, statuses)
        ),
        [kb.booking_menu_back_button],
        [kb.hide_keyboard_button],
    )

    await utils.try_edit_or_answer(callback.message, hbold("Your accounts:"), keyboard)


@router.callback_query(BookingCallbackData.filter(F.action == BookingAction.stop))
async def stop_booking(callback: CallbackQuery, callback_data: BookingCallbackData):
    account = service.get_booking_account_by_id(callback_data.account_id)
    await booking.stop_booking(account.email, account.password)
    await utils.try_delete_message(callback.message)
    await get_booking_accounts(callback)


@router.callback_query(BookingCallbackData.filter(F.action == BookingAction.run))
async def run_booking(callback: CallbackQuery, callback_data: BookingCallbackData):
    account = service.get_booking_account_by_id(callback_data.account_id)
    await booking.run_booking(account.email, account.password)
    await utils.try_delete_message(callback.message)
    await get_booking_accounts(callback)


# Fill
@router.callback_query(F.data == "submit_booking_account")
async def submit_booking_account(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    email = data["email"]
    password = data["password"]

    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

    if not re.fullmatch(email_regex, email):
        return await callback.answer("Not valid email")

    user = utils.get_user(callback.message)

    if email in (acc.email for acc in user.booking_accounts):
        return await callback.answer("Account with that email already exist")

    service.create_booking_account(user, email, password)

    await state.clear()
    await state.set_state(BaseState.none)
    await utils.try_delete_message(callback.message)
    await get_booking_accounts(callback)


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
