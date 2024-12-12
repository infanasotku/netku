from abc import abstractmethod


from app.contracts.services.base import BaseService


class BookingAnalysisService(BaseService):
    @abstractmethod
    async def get_booked_machine_count_by_user_telegram_id(
        self, telegram_id: int
    ) -> int:
        """Counts booking accounts which
        booked corresponding machines for specified user.

        :return: Count of booked machines for user."""
