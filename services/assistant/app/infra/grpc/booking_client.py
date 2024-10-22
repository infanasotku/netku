from abc import ABC, abstractmethod

from app.infra.grpc.gen.booking_pb2_grpc import BookingStub
from app.infra.grpc.gen.booking_pb2 import BookingRequest, BookingResponse

from app.infra.grpc.grpc_client import GRPCClient


class AbstractBookingClient(ABC):
    @abstractmethod
    async def run_booking(self, email: str, password: str):
        pass

    @abstractmethod
    async def stop_booking(self, email: str, password: str):
        pass

    @abstractmethod
    async def booked(self, email: str, password: str) -> bool:
        pass


class BookingClient(GRPCClient, AbstractBookingClient):
    async def run_booking(self, email: str, password: str):
        ch = await self.get_channel()
        if ch is None:
            return

        stub = BookingStub(ch)
        await stub.RunBooking(BookingRequest(email=email, password=password))

    async def stop_booking(self, email: str, password: str):
        ch = await self.get_channel()
        if ch is None:
            return

        stub = BookingStub(ch)
        await stub.StopBooking(BookingRequest(email=email, password=password))

    async def booked(self, email: str, password: str) -> bool:
        ch = await self.get_channel()
        if ch is None:
            return

        stub = BookingStub(ch)
        resp: BookingResponse = await stub.Booked(
            BookingRequest(email=email, password=password)
        )
        return bool(resp.booked)
