# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""

import grpc

from health.gen import health_pb2 as health_dot_gen_dot_health__pb2

GRPC_GENERATED_VERSION = "1.66.0"
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower

    _version_not_supported = first_version_is_lower(
        GRPC_VERSION, GRPC_GENERATED_VERSION
    )
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f"The grpc package installed is at version {GRPC_VERSION},"
        + " but the generated code in health/gen/health_pb2_grpc.py depends on"
        + f" grpcio>={GRPC_GENERATED_VERSION}."
        + f" Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}"
        + f" or downgrade your generated code using grpcio-tools<={GRPC_VERSION}."
    )


class HealthStub(object):
    """Health is gRPC's mechanism for checking whether a server is able to handle
    RPCs. Its semantics are documented in
    https://github.com/grpc/grpc/blob/master/doc/health-checking.md.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Check = channel.unary_unary(
            "/grpc.health.v1.Health/Check",
            request_serializer=health_dot_gen_dot_health__pb2.HealthCheckRequest.SerializeToString,
            response_deserializer=health_dot_gen_dot_health__pb2.HealthCheckResponse.FromString,
            _registered_method=True,
        )
        self.Watch = channel.unary_stream(
            "/grpc.health.v1.Health/Watch",
            request_serializer=health_dot_gen_dot_health__pb2.HealthCheckRequest.SerializeToString,
            response_deserializer=health_dot_gen_dot_health__pb2.HealthCheckResponse.FromString,
            _registered_method=True,
        )


class HealthServicer(object):
    """Health is gRPC's mechanism for checking whether a server is able to handle
    RPCs. Its semantics are documented in
    https://github.com/grpc/grpc/blob/master/doc/health-checking.md.
    """

    def Check(self, request, context):
        """Check gets the health of the specified service. If the requested service
        is unknown, the call will fail with status NOT_FOUND. If the caller does
        not specify a service name, the server should respond with its overall
        health status.

        Clients should set a deadline when calling Check, and can declare the
        server unhealthy if they do not receive a timely response.

        Check implementations should be idempotent and side effect free.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Watch(self, request, context):
        """Performs a watch for the serving status of the requested service.
        The server will immediately send back a message indicating the current
        serving status.  It will then subsequently send a new message whenever
        the service's serving status changes.

        If the requested service is unknown when the call is received, the
        server will send a message setting the serving status to
        SERVICE_UNKNOWN but will *not* terminate the call.  If at some
        future point, the serving status of the service becomes known, the
        server will send a new message with the service's serving status.

        If the call terminates with status UNIMPLEMENTED, then clients
        should assume this method is not supported and should not retry the
        call.  If the call terminates with any other status (including OK),
        clients should retry the call with appropriate exponential backoff.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_HealthServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Check": grpc.unary_unary_rpc_method_handler(
            servicer.Check,
            request_deserializer=health_dot_gen_dot_health__pb2.HealthCheckRequest.FromString,
            response_serializer=health_dot_gen_dot_health__pb2.HealthCheckResponse.SerializeToString,
        ),
        "Watch": grpc.unary_stream_rpc_method_handler(
            servicer.Watch,
            request_deserializer=health_dot_gen_dot_health__pb2.HealthCheckRequest.FromString,
            response_serializer=health_dot_gen_dot_health__pb2.HealthCheckResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "grpc.health.v1.Health", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers("grpc.health.v1.Health", rpc_method_handlers)


# This class is part of an EXPERIMENTAL API.
class Health(object):
    """Health is gRPC's mechanism for checking whether a server is able to handle
    RPCs. Its semantics are documented in
    https://github.com/grpc/grpc/blob/master/doc/health-checking.md.
    """

    @staticmethod
    def Check(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/grpc.health.v1.Health/Check",
            health_dot_gen_dot_health__pb2.HealthCheckRequest.SerializeToString,
            health_dot_gen_dot_health__pb2.HealthCheckResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def Watch(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_stream(
            request,
            target,
            "/grpc.health.v1.Health/Watch",
            health_dot_gen_dot_health__pb2.HealthCheckRequest.SerializeToString,
            health_dot_gen_dot_health__pb2.HealthCheckResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )
