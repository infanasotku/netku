from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext


def create_inline_keyboard(
    *layers: list[InlineKeyboardButton],
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[layer for layer in layers])


hide_keyboard_button = InlineKeyboardButton(text="Hide", callback_data="hide_keyboard")

booking_account_creating_button = InlineKeyboardButton(
    text="Add account", callback_data="create_booking_account_menu"
)
booking_accounts_getting_button = InlineKeyboardButton(
    text="Accounts", callback_data="get_booking_accounts"
)
booking_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [booking_accounts_getting_button],
        [booking_account_creating_button],
        [hide_keyboard_button],
    ]
)


async def generate_booking_account_creating_menu(state: FSMContext):
    data = await state.get_data()
    email = data.get("email")
    password = data.get("password")

    return create_inline_keyboard(
        [
            InlineKeyboardButton(
                text=email if email else "Email", callback_data="fill_booking_email"
            )
        ],
        [
            InlineKeyboardButton(
                text=password if password else "Password",
                callback_data="fill_booking_password",
            )
        ],
        [
            *(
                [
                    InlineKeyboardButton(
                        text="Submit",
                        callback_data="submit_booking_account",
                    )
                ]
                if email and password
                else []
            )
        ],
        [
            InlineKeyboardButton(
                text="Back",
                callback_data="get_booking_menu",
            ),
        ],
        [hide_keyboard_button],
    )


booking_account_creating_menu = create_inline_keyboard(
    [booking_accounts_getting_button],
    [booking_account_creating_button],
    [
        InlineKeyboardButton(
            text="Back",
            callback_data="get_booking_menu",
        ),
    ],
    [hide_keyboard_button],
)
