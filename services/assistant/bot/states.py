from aiogram.fsm.state import StatesGroup, State


class BaseState(StatesGroup):
    none = State()
    registration = State()
