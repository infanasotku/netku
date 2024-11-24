from app.contracts.services import BookingAnalysisService, BookingService, UserService


class BookingAnalysisServiceImpl(BookingAnalysisService):
    def __init__(self, booking_service: BookingService, user_service: UserService):
        self._booking_service = booking_service
        self._user_service = user_service

    async def get_booked_machine_count_by_user_telegram_id(
        self, telegram_id: int
    ) -> int:
        user = await self._user_service.get_user_by_telegram_id(telegram_id)
        if user is None:
            return 0

        return sum(
            [
                1
                if await self._booking_service.booked(account.email, account.password)
                else 0
                for account in user.booking_accounts
            ]
        )
