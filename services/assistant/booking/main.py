import grpc

import health
from settings import settings

from booking.gen.booking_pb2_grpc import BookingStub
from booking.gen.booking_pb2 import BookingRequest


class Booking:
    def __init__(self):
        # Displayed booking status email: status
        # Machine is booked if status = True
        self._statuses: dict[str, bool] = {}

    async def run_booking(self, email: str, password: str):
        if not await health.wait_healthy(
            "booking", f"{settings.booking_host}:{settings.booking_port}"
        ):
            return

        async with grpc.aio.insecure_channel(
            f"{settings.booking_host}:{settings.booking_port}"
        ) as ch:
            stub = BookingStub(ch)
            await stub.RunBooking(BookingRequest(email=email, password=password))
            self._statuses[email] = True

    async def stop_booking(self, email: str, password: str):
        if not await health.wait_healthy(
            "booking", f"{settings.booking_host}:{settings.booking_port}"
        ):
            return

        async with grpc.aio.insecure_channel(
            f"{settings.booking_host}:{settings.booking_port}"
        ) as ch:
            stub = BookingStub(ch)
            await stub.StopBooking(BookingRequest(email=email, password=password))
            self._statuses[email] = False

    def booked(self, email: str) -> bool:
        """Returns booking status, `True` if machine booked, `False` otherwise"""
        return self._statuses.get(email, False)
