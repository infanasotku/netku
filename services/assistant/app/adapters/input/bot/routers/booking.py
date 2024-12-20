from logging import Logger
import re
from aiogram import Dispatcher, Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from app.contracts.protocols import CreateService
from app.contracts.services import (
    BookingAnalysisService,
    BookingService,
    UserService,
)

from app.schemas.booking import BookingAccountCreateSchema

from app.adapters.input.bot.states import BaseState, BookingAccountAdding
import app.adapters.input.bot.utils as utils
import app.adapters.input.bot.text as text
import app.adapters.input.bot.kb as kb
from app.adapters.input.bot.schemas import BookingCallbackData, BookingAction

from app.adapters.input.bot.routers.base import BaseRouter


class BookingRouter(BaseRouter):
    def __init__(
        self,
        create_booking_service: CreateService[BookingService],
        create_user_service: CreateService[UserService],
        create_booking_analysis_service: CreateService[BookingAnalysisService],
        logger: Logger,
    ):
        self.create_booking_service = create_booking_service
        self.create_user_service = create_user_service
        self.create_booking_analysis_service = create_booking_analysis_service
        self.router = Router(name="main")
        self.logger = logger

    def register_router(self, dp: Dispatcher):
        self._register_handlers()
        dp.include_router(self.router)

    def _register_handlers(self):
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

    async def _get_booking_menu(
        self, message: Message | CallbackQuery, state: FSMContext
    ):
        await state.set_state(BaseState.none)
        if isinstance(message, CallbackQuery):
            message = message.message

        async with (
            self.create_user_service() as user_service,
            self.create_booking_analysis_service() as booking_analysis,
        ):
            user = await user_service.get_user_by_telegram_id(message.chat.id)

            if not user:
                return await message.answer(text.please_click_start)

            booked_count = (
                await booking_analysis.get_booked_machine_count_by_user_telegram_id(
                    message.chat.id
                )
            )

            await utils.try_edit_or_answer(
                message,
                f"Now booked: {booked_count}",
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
            user = await user_service.get_user_by_telegram_id(callback.message.chat.id)

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
                self.logger.warning(f"Booking starting failed [{account.email}].")
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
            user = await user_service.get_user_by_telegram_id(callback.message.chat.id)

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
