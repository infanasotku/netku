import asyncio
from logging import Logger
import re
from typing import AsyncContextManager, Callable
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

from app.contracts.services import (
    BookingAnalysisService,
    BookingService,
    UserService,
    XrayService,
)

from app.schemas.booking import BookingAccountCreateSchema

from app.adapters.bot.states import BaseState, BookingAccountAdding
import app.adapters.bot.utils as utils
import app.adapters.bot.text as text
import app.adapters.bot.kb as kb
from app.adapters.bot.schemas import BookingCallbackData, BookingAction


class MainRouter:
    def __init__(
        self,
        create_booking_service: Callable[[], AsyncContextManager[BookingService]],
        create_user_service: Callable[[], AsyncContextManager[UserService]],
        create_xray_service: Callable[[], AsyncContextManager[XrayService]],
        create_booking_analysis_service: Callable[
            [], AsyncContextManager[BookingAnalysisService]
        ],
        logger: Logger,
    ):
        self.create_booking_service = create_booking_service
        self.create_user_service = create_user_service
        self.create_xray_service = create_xray_service
        self.create_booking_analysis_service = create_booking_analysis_service
        self.router = Router(name="main")
        self.logger = logger

    def register_router(self, dp: Dispatcher):
        self._register_handlers()
        dp.include_router(self.router)

    def _register_handlers(self):
        self.router.message.register(self._start, Command("start"))
        self.router.message.register(self._stop, Command("stop"))
        self.router.message.register(self._stop, BaseState.registration)

        # Proxy
        self.router.message.register(self._subscribe_for_proxy, Command("proxy"))
        self.router.message.register(self._get_proxy_uuid, Command("proxy_uid"))

        # Booking
        self.router.callback_query.register(
            self._get_booking_menu, F.data == "get_booking_menu"
        )
        self.router.message.register(self._get_booking_menu, Command("machine_booking"))
        self.router.callback_query.register(
            self._get_booking_account_creating_menu,
            F.data == "create_booking_account_menu",
        )
        self.router.callback_query.register(
            self._get_booking_accounts, F.data == "get_booking_accounts"
        )
        self.router.callback_query.register(
            self._stop_booking,
            BookingCallbackData.filter(F.action == BookingAction.stop),
        )
        self.router.callback_query.register(
            self._run_booking, BookingCallbackData.filter(F.action == BookingAction.run)
        )
        self.router.callback_query.register(
            self._submit_booking_account, F.data == "submit_booking_account"
        )
        self.router.callback_query.register(
            self._fill_booking_email, F.data == "fill_booking_email"
        )
        self.router.message.register(
            self._apply_booking_email, BookingAccountAdding.email
        )
        self.router.callback_query.register(
            self._fill_booking_password, F.data == "fill_booking_password"
        )
        self.router.message.register(
            self._apply_booking_password, BookingAccountAdding.password
        )

        # Common
        self.router.callback_query.register(
            self._hide_keyboard, F.data == "hide_keyboard"
        )
        self.router.message.register(self._delete_extra, BaseState.none)
        self.router.error.register(self._error_handler)

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
        self, message: Message | CallbackQuery, state: FSMContext
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
            if not await booking_service.run_booking(account.email, account.password):
                await callback.answer("Booking starting failed")
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
            await booking_service.create_booking_account(
                BookingAccountCreateSchema(
                    owner_id=user.id, email=email, password=password
                )
            )

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
