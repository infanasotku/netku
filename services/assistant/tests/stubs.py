from app.contracts.clients import XrayClient, BookingClient, AssistantClient
from app.contracts.repositories import XrayRepository, AvailabilityRepository
from app.contracts.services import UserService


class StubXrayRepository(XrayRepository):
    async def get_last_xray_record(self):
        raise NotImplementedError

    async def create_xray_record(self, account_create):
        raise NotImplementedError

    async def update_xray_record(self, user_id, user_update):
        raise NotImplementedError


class StubXrayClient(XrayClient):
    async def check_health(self):
        raise NotImplementedError

    async def restart(self):
        raise NotImplementedError


class StubAvailabilityRepository(AvailabilityRepository):
    async def get_availability_by_id(self, id):
        raise NotImplementedError

    async def log_availability(self, availability_create):
        raise NotImplementedError


class StubBookingClient(BookingClient):
    async def check_health(self):
        raise NotImplementedError

    async def run_booking(self, email, password):
        raise NotImplementedError

    async def stop_booking(self, email, password):
        raise NotImplementedError

    async def booked(self, email, password):
        raise NotImplementedError


class StubAssistantClient(AssistantClient):
    async def check_health(self):
        raise NotImplementedError


class StubUserService(UserService):
    async def get_user_by_telegram_id(self, id):
        raise NotImplementedError

    async def get_user_by_phone(self, phone):
        raise NotImplementedError

    async def get_users(self):
        raise NotImplementedError

    async def update_user(self, user_id, user_update):
        raise NotImplementedError

    async def get_users_by_active_subscriptions(self, subscriptions, every=False):
        raise NotImplementedError

    async def send_notify_by_subscriptions(self, subscriptions, message):
        raise NotImplementedError
