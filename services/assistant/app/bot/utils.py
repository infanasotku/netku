from typing import Any, Callable, Coroutine
from collections import Counter
from aiogram.types import Message, Contact, InlineKeyboardButton
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from app.schemas.user_schemas import UserSchema
from app.services import AbstractUserService, AbstractBookingService

import app.bot.kb as kb
from app.bot.states import BaseState


async def try_delete_message(message: Message) -> bool:
    """
    Tries to delete message, return `True`
    if the `message` successfully deleted, `False` otherwise.
    """
    try:
        await message.delete()
        return True
    except Exception:
        return False


async def try_edit_message(
    message: Message, text: str, reply_markup: Any = None
) -> bool:
    """
    Tries to edit message. Return `True`
    if the `message` successfully edited, `False` otherwise.
    """
    try:
        await message.edit_text(text=text, reply_markup=reply_markup)
        return True
    except Exception:
        return False


async def try_edit_or_answer(message: Message, text: str, reply_markup: Any = None):
    """
    Tries to edit message.
    if the `message` unsuccessfully edited
    then answers message by `Message.answer_text`.

    Returns: `True` if message edited, `False` otherwise.
    """
    if not await try_edit_message(
        message=message, text=text, reply_markup=reply_markup
    ):
        await message.answer(text=text, reply_markup=reply_markup)
        return False

    return True


async def fill_field(
    message: Message,
    state: FSMContext,
    fieldname: str,
    back_button: InlineKeyboardButton,
    fill_state: State,
):
    await state.set_state(fill_state)
    await state.update_data(msg=message)
    text = back_button.text
    back_button.text = "Back"
    await try_edit_or_answer(
        message,
        hbold(f"Input {fieldname}:"),
        kb.create_inline_keyboard([back_button]),
    )
    back_button.text = text


async def apply_field(
    message: Message,
    state: FSMContext,
    fieldname: str,
    menu_text: str,
    menu_generator: Callable[[FSMContext], Coroutine],
):
    await state.set_state(BaseState.none)
    data = await state.get_data()
    await state.update_data({fieldname: message.text})
    msg: Message = data["msg"]
    await try_delete_message(message)
    await try_edit_or_answer(msg, menu_text, await menu_generator(state))


async def get_user(
    message: Message, user_service: AbstractUserService
) -> UserSchema | None:
    """Finds user by `message.chat.id`
    - Returns `UserSchema` if user exist,
    `None` otherwise."""
    return await user_service.get_user_by_telegram_id(message.chat.id)


async def registrate_user(
    contact: Contact, user_service: AbstractUserService
) -> UserSchema | None:
    """Registrates user by `contact.user_id` and `contact.phone_number`
    - Returns `UserSchema` if user registrated successful
    (User registrated successful if he founded by his `contact.phone_number` in db
    ), `None` otherwise."""
    user = await user_service.get_user_by_phone(contact.phone_number)
    if not user:
        return

    user.telegram_id = contact.user_id
    await user_service.update_user(user)
    return user


async def subscribe_user(
    user: UserSchema, subscription: str, user_service: AbstractUserService
):
    """Subscribes user to `subscription`."""
    match subscription:
        case "proxy":
            user.proxy_subscription = True

    await user_service.update_user(user)


async def unsubscribe_user(
    user: UserSchema, subscription: str, user_service: AbstractUserService
):
    """Unsubscribes user from `subscription`."""
    match subscription:
        case "proxy":
            user.proxy_subscription = False
        case "all":
            user.proxy_subscription = False

    await user_service.update_user(user)


async def get_booking_machine_count(
    message: Message,
    user_service: AbstractUserService,
    booking_service: AbstractBookingService,
) -> int:
    user = await get_user(message, user_service)
    if user is None:
        return 0

    return Counter(
        [
            await booking_service.booked(account.email, account.password)
            for account in user.booking_accounts
        ]
    )[True]
