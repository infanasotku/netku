from app.contracts.clients import BookingClient

from app.adapters.output.grpc.gen.booking_pb2_grpc import BookingStub
from app.adapters.output.grpc.gen.booking_pb2 import BookingRequest, BookingResponse

from app.adapters.output.grpc.base import GRPCClient


class GRPCBookingClient(GRPCClient, BookingClient):
    service_name = "booking"

    async def run_booking(self, email: str, password: str) -> bool:
        healthy = await self.check_health()
        if not healthy:
            return

        stub = BookingStub(self._channel)
        await stub.RunBooking(BookingRequest(email=email, password=password))
        return True

    async def stop_booking(self, email: str, password: str):
        healthy = await self.check_health()
        if not healthy:
            return

        stub = BookingStub(self._channel)
        await stub.StopBooking(BookingRequest(email=email, password=password))

    async def booked(self, email: str, password: str) -> bool:
        healthy = await self.check_health()
        if not healthy:
            return

        stub = BookingStub(self._channel)
        resp: BookingResponse = await stub.Booked(
            BookingRequest(email=email, password=password)
        )
        return bool(resp.booked)
