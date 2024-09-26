import grpc

import health
from settings import settings

from booking.gen.booking_pb2_grpc import BookingStub
from booking.gen.booking_pb2 import BookingRequest, BookingResponse


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

    async def booked(self, email: str, password: str) -> bool:
        """Returns booking status, `True` if machine booked, `False` otherwise"""
        if not await health.check_service(
            "booking", f"{settings.booking_host}:{settings.booking_port}"
        ):
            return False

        async with grpc.aio.insecure_channel(
            f"{settings.booking_host}:{settings.booking_port}"
        ) as ch:
            stub = BookingStub(ch)
            resp: BookingResponse = await stub.Booked(
                BookingRequest(email=email, password=password)
            )
            return bool(resp.booked)
