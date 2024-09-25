import grpc

import health
from settings import settings

from booking.gen.booking_pb2_grpc import BookingStub
from booking.gen.booking_pb2 import BookingRequest


class Booking:
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
