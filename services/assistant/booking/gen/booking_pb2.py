# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: booking/gen/booking.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 27, 2, "", "booking/gen/booking.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x19\x62ooking/gen/booking.proto\x12\x07\x62ooking"1\n\x0e\x42ookingRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t"!\n\x0f\x42ookingResponse\x12\x0e\n\x06\x62ooked\x18\x01 \x01(\x08\x32\xcf\x01\n\x07\x42ooking\x12\x41\n\nRunBooking\x12\x17.booking.BookingRequest\x1a\x18.booking.BookingResponse"\x00\x12\x42\n\x0bStopBooking\x12\x17.booking.BookingRequest\x1a\x18.booking.BookingResponse"\x00\x12=\n\x06\x42ooked\x12\x17.booking.BookingRequest\x1a\x18.booking.BookingResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "booking.gen.booking_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_BOOKINGREQUEST"]._serialized_start = 38
    _globals["_BOOKINGREQUEST"]._serialized_end = 87
    _globals["_BOOKINGRESPONSE"]._serialized_start = 89
    _globals["_BOOKINGRESPONSE"]._serialized_end = 122
    _globals["_BOOKING"]._serialized_start = 125
    _globals["_BOOKING"]._serialized_end = 332
# @@protoc_insertion_point(module_scope)
