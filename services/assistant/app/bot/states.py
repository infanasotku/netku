from aiogram.fsm.state import StatesGroup, State


class BaseState(StatesGroup):
    none = State()
    registration = State()


class BookingAccountAdding(StatesGroup):
    email = State()
    password = State()
