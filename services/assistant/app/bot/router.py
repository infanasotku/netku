import asyncio
from logging import Logger
import re
from typing import AsyncContextManager, Callable, Union
from aiogram import Dispatcher, Router, F
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

from app.services import (
    AbstractBookingService,
    AbstractUserService,
    AbstractXrayService,
)

from app.bot.states import BaseState, BookingAccountAdding
import app.bot.utils as utils
import app.bot.text as text
import app.bot.kb as kb
from app.bot.schemas import BookingCallbackData, BookingAction


class MainRouter:
    def __init__(
        self,
        create_booking_service: Callable[
            [], AsyncContextManager[AbstractBookingService]
        ],
        create_user_service: Callable[[], AsyncContextManager[AbstractUserService]],
        create_xray_service: Callable[[], AsyncContextManager[AbstractXrayService]],
        logger: Logger,
    ):
        self.create_booking_service = create_booking_service
        self.create_user_service = create_user_service
        self.create_xray_service = create_xray_service
        self.router = Router(name="main")
        self.logger = logger

    def register_router(self, dp: Dispatcher):
        self._register_handlers()
        dp.include_router(self.router)

    def _register_handlers(self):
        self.router.message(Command("start"))(self._start)
        self.router.message(Command("stop"))(self._stop)
        self.router.message(BaseState.registration)(self._registrate)

        # Proxy
        self.router.message(Command("proxy"))(self._subscribe_for_proxy)
        self.router.message(Command("proxy_uid"))(self._get_proxy_uuid)

        # Booking
        self.router.callback_query(F.data == "get_booking_menu")(
            self.router.message(Command("machine_booking"))(self._get_booking_menu)
        )
        self.router.callback_query(F.data == "create_booking_account_menu")(
            self._get_booking_account_creating_menu
        )
        self.router.callback_query(F.data == "get_booking_accounts")(
            self._get_booking_accounts
        )
        self.router.callback_query(
            BookingCallbackData.filter(F.action == BookingAction.stop)
        )(self._stop_booking)
        self.router.callback_query(
            BookingCallbackData.filter(F.action == BookingAction.run)
        )(self._run_booking)
        self.router.callback_query(F.data == "submit_booking_account")(
            self._submit_booking_account
        )
        self.router.callback_query(F.data == "fill_booking_email")(
            self._fill_booking_email
        )
        self.router.message(BookingAccountAdding.email)(self._apply_booking_email)
        self.router.callback_query(F.data == "fill_booking_password")(
            self._fill_booking_password
        )
        self.router.message(BookingAccountAdding.password)(self._apply_booking_password)

        # Common
        self.router.callback_query(F.data == "hide_keyboard")(self._hide_keyboard)
        self.router.message(BaseState.none)(self._delete_extra)
        self.router.error()(self._error_handler)

    async def _start(self, message: Message, state: FSMContext):
        async with self.create_user_service() as user_service:
            user = await utils.get_user(message, user_service)

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
            user = await utils.get_user(message, user_service)

            if not user:
                return await message.answer(text.please_click_start)

            await utils.unsubscribe_user(user, "all", user_service)

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

    # region Services

    # region Proxy
    async def _subscribe_for_proxy(self, message: Message):
        async with self.create_user_service() as user_service:
            user = await utils.get_user(message, user_service)

            if not user:
                return await message.answer(text.please_click_start)

            if user.proxy_subscription:
                return await message.answer("You already subscribeted to proxy!")

            await utils.subscribe_user(user, "proxy", user_service)

        await message.answer("You subscribeted to proxy!")

    async def _get_proxy_uuid(self, message: Message):
        async with self.create_user_service() as user_service:
            user = await utils.get_user(message, user_service)

        if not user:
            return await message.answer(text.please_click_start)

        if not user.proxy_subscription:
            return await message.answer("You didn't subscribe to proxy!")

        async with self.create_xray_service() as xray_service:
            uid = await xray_service.get_current_uid()

        if not uid:
            return await message.answer(hbold("Proxy inactive"))

        return await message.answer(hbold(uid))

    # endregion

    # region Booking
    async def _get_booking_menu(
        self, message: Union[Message, CallbackQuery], state: FSMContext
    ):
        await state.set_state(BaseState.none)
        if isinstance(message, CallbackQuery):
            message = message.message

        async with (
            self.create_user_service() as user_service,
            self.create_booking_service() as booking_service,
        ):
            user = await utils.get_user(message, user_service)

            if not user:
                return await message.answer(text.please_click_start)

            await utils.try_edit_or_answer(
                message,
                f"Now booked: {await utils.get_booking_machine_count(message, user_service, booking_service)}",
                kb.booking_menu,
            )

    async def _get_booking_account_creating_menu(
        self, callback: CallbackQuery, state: FSMContext
    ):
        await state.set_state(BaseState.none)
        await utils.try_edit_or_answer(
            callback.message,
            text.create_booking_account_text,
            await kb.generate_booking_account_creating_menu(state),
        )

    async def _get_booking_accounts(self, callback: CallbackQuery):
        async with self.create_user_service() as user_service:
            user = await utils.get_user(callback.message, user_service)

        accounts = user.booking_accounts

        if len(accounts) == 0:
            return await callback.answer("You haven't accounts")

        async with self.create_booking_service() as booking_service:
            statuses = [
                await booking_service.booked(acc.email, acc.password)
                for acc in accounts
            ]

        keyboard = kb.create_inline_keyboard(
            *(
                [
                    InlineKeyboardButton(text=account.email, callback_data="stub"),
                    InlineKeyboardButton(
                        text="Run" if not status else "Stop",
                        callback_data=BookingCallbackData(
                            user_id=user.id,
                            account_id=account.id,
                            action=BookingAction.run
                            if not status
                            else BookingAction.stop,
                        ).pack(),
                    ),
                ]
                for account, status in zip(accounts, statuses)
            ),
            [kb.booking_menu_back_button],
            [kb.hide_keyboard_button],
        )

        await utils.try_edit_or_answer(
            callback.message, hbold("Your accounts:"), keyboard
        )

    async def _stop_booking(
        self, callback: CallbackQuery, callback_data: BookingCallbackData
    ):
        async with self.create_booking_service() as booking_service:
            account = await booking_service.get_booking_account_by_id(
                callback_data.account_id
            )
            await booking_service.stop_booking(account.email, account.password)
            await utils.try_delete_message(callback.message)
            await self._get_booking_accounts(callback)

    async def _run_booking(
        self, callback: CallbackQuery, callback_data: BookingCallbackData
    ):
        async with self.create_booking_service() as booking_service:
            account = await booking_service.get_booking_account_by_id(
                callback_data.account_id
            )
            await booking_service.run_booking(account.email, account.password)
            await utils.try_delete_message(callback.message)
            await self._get_booking_accounts(callback)

    # Fill
    async def _submit_booking_account(self, callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        email = data["email"]
        password = data["password"]

        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

        if not re.fullmatch(email_regex, email):
            return await callback.answer("Not valid email")

        async with self.create_user_service() as user_service:
            user = await utils.get_user(callback.message, user_service)

        if email in (acc.email for acc in user.booking_accounts):
            return await callback.answer("Account with that email already exist")

        async with self.create_booking_service() as booking_service:
            await booking_service.create_booking_account(user, email, password)

        await state.clear()
        await state.set_state(BaseState.none)
        await utils.try_delete_message(callback.message)
        await self._get_booking_accounts(callback)

    async def _fill_booking_email(self, callback: CallbackQuery, state: FSMContext):
        await utils.fill_field(
            callback.message,
            state,
            "email",
            kb.booking_account_creating_button,
            BookingAccountAdding.email,
        )

    async def _apply_booking_email(self, message: Message, state: FSMContext):
        await utils.apply_field(
            message,
            state,
            "email",
            text.create_booking_account_text,
            kb.generate_booking_account_creating_menu,
        )

    async def _fill_booking_password(self, callback: CallbackQuery, state: FSMContext):
        await utils.fill_field(
            callback.message,
            state,
            "password",
            kb.booking_account_creating_button,
            BookingAccountAdding.password,
        )

    async def _apply_booking_password(self, message: Message, state: FSMContext):
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
