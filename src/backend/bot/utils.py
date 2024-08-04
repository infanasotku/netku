from typing import Any
from aiogram.types import Message, Contact

from db.schemas import UserSchema


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


def get_user(message: Message) -> UserSchema | None:
    """Finds user by `message.chat.id`

    - Returns `UserSchema` if user and his `UserSchema.telegram_id` exist,
    `None` otherwise."""
    return


def registrate_user(contact: Contact) -> UserSchema | None:
    """Registrates user by `contact.user_id` and `contact.phone_number`

    - Returns `UserSchema` if user registrated successful
    (User registrated successful if he founded by his `contact.phone_number` in db
    ), `None` otherwise."""
    print(contact.phone_number)
    return UserSchema(id=None, phone_number=None, telegram_id=None)
