import asyncio
from logging import Logger
from aiogram import Dispatcher, Router, F
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

from app.contracts.protocols import CreateService
from app.contracts.services import (
    UserService,
)

from app.schemas.user import Subscription

from app.adapters.input.bot.states import BaseState
import app.adapters.input.bot.utils as utils
import app.adapters.input.bot.text as text

from app.adapters.input.bot.routers.base import BaseRouter


class MainRouter(BaseRouter):
    def __init__(
        self,
        create_user_service: CreateService[UserService],
        logger: Logger,
    ):
        self.create_user_service = create_user_service
        self.router = Router(name="main")
        self.logger = logger

    def register_router(self, dp: Dispatcher):
        self._register_handlers()
        dp.include_router(self.router)

    def _register_handlers(self):
        self.router.message.register(self._start, Command("start"))
        self.router.message.register(self._stop, Command("stop"))
        self.router.message.register(self._stop, BaseState.registration)

        # Availability
        self.router.message.register(
            self._subscribe_for_availability, Command("availability")
        )

        # Common
        self.router.callback_query.register(
            self._hide_keyboard, F.data == "hide_keyboard"
        )
        self.router.message.register(self._delete_extra, BaseState.none)
        self.router.error.register(self._error_handler)

    async def _start(self, message: Message, state: FSMContext):
        async with self.create_user_service() as user_service:
            user = await user_service.get_user_by_telegram_id(message.chat.id)

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

    async def _stop(self, message: Message):
        async with self.create_user_service() as user_service:
            user = await user_service.get_user_by_telegram_id(message.chat.id)

            if not user:
                return await message.answer(text.please_click_start)

            for subs in Subscription:
                await utils.unsubscribe_user(user, subs, user_service)

        await message.answer("Subscriptions canceled!")

    async def _registrate(self, message: Message):
        if not message.contact:
            return await utils.try_delete_message(message)

        async with self.create_user_service() as user_service:
            user = await utils.registrate_user(message.contact, user_service)
        if user:
            await message.answer(
                "Registration successful!", reply_markup=ReplyKeyboardRemove()
            )
        if not user:
            await message.answer(
                "Sorry, you have not enough permissions for registration.",
                reply_markup=ReplyKeyboardRemove(),
            )

    # region Availability
    async def _subscribe_for_availability(self, message: Message):
        async with self.create_user_service() as user_service:
            user = await user_service.get_user_by_telegram_id(message.chat.id)

            if not user:
                return await message.answer(text.please_click_start)

            if user.availability_subscription:
                return await message.answer("You already subscribeted to availability!")

            await utils.subscribe_user(
                user, Subscription.availability_subscription, user_service
            )

        await message.answer("You subscribeted to availability!")

    # endregion

    # region Common
    async def _hide_keyboard(self, callback: CallbackQuery):
        if not await utils.try_delete_message(callback.message):
            await callback.message.answer("Keyboard too old")

    async def _delete_extra(self, message: Message):
        await utils.try_delete_message(message)

    async def _error_handler(self, event: ErrorEvent):
        self.logger.error(f"Error occurred: {event.exception}")
        message = event.update.callback_query.message
        await utils.try_delete_message(message)
        msg = await message.answer(
            "Error occurred! Contact your admin.", reply_markup=ReplyKeyboardRemove()
        )
        await asyncio.sleep(3)
        await msg.delete()

    # endregion
