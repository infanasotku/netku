from aiogram.filters.callback_data import CallbackData
from enum import Enum


class BookingAction(str, Enum):
    stop = 1
    run = 2


class BookingCallbackData(CallbackData, prefix="booking"):
    user_id: int
    account_id: int
    action: BookingAction
