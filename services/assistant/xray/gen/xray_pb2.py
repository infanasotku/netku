# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: xray/gen/xray.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 27, 2, "", "xray/gen/xray.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x13xray/gen/xray.proto\x12\x04xray"\x1f\n\x0fRestartResponse\x12\x0c\n\x04uuid\x18\x01 \x01(\t"\x06\n\x04Null2A\n\x0bXrayService\x12\x32\n\x0bRestartXray\x12\n.xray.Null\x1a\x15.xray.RestartResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "xray.gen.xray_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_RESTARTRESPONSE"]._serialized_start = 29
    _globals["_RESTARTRESPONSE"]._serialized_end = 60
    _globals["_NULL"]._serialized_start = 62
    _globals["_NULL"]._serialized_end = 68
    _globals["_XRAYSERVICE"]._serialized_start = 70
    _globals["_XRAYSERVICE"]._serialized_end = 135
# @@protoc_insertion_point(module_scope)
