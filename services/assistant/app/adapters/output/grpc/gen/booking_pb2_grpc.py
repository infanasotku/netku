# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from app.adapters.output.grpc.gen import booking_pb2 as app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2

GRPC_GENERATED_VERSION = '1.67.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in app/adapters/output/grpc/gen/booking_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class BookingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RunBooking = channel.unary_unary(
                '/Booking/RunBooking',
                request_serializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingRequest.SerializeToString,
                response_deserializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingResponse.FromString,
                _registered_method=True)
        self.StopBooking = channel.unary_unary(
                '/Booking/StopBooking',
                request_serializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingRequest.SerializeToString,
                response_deserializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingResponse.FromString,
                _registered_method=True)
        self.Booked = channel.unary_unary(
                '/Booking/Booked',
                request_serializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingRequest.SerializeToString,
                response_deserializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingResponse.FromString,
                _registered_method=True)


class BookingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RunBooking(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StopBooking(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Booked(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BookingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RunBooking': grpc.unary_unary_rpc_method_handler(
                    servicer.RunBooking,
                    request_deserializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingRequest.FromString,
                    response_serializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingResponse.SerializeToString,
            ),
            'StopBooking': grpc.unary_unary_rpc_method_handler(
                    servicer.StopBooking,
                    request_deserializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingRequest.FromString,
                    response_serializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingResponse.SerializeToString,
            ),
            'Booked': grpc.unary_unary_rpc_method_handler(
                    servicer.Booked,
                    request_deserializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingRequest.FromString,
                    response_serializer=app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Booking', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Booking', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Booking(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RunBooking(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Booking/RunBooking',
            app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingRequest.SerializeToString,
            app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def StopBooking(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Booking/StopBooking',
            app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingRequest.SerializeToString,
            app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Booked(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Booking/Booked',
            app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingRequest.SerializeToString,
            app_dot_adapters_dot_output_dot_grpc_dot_gen_dot_booking__pb2.BookingResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
