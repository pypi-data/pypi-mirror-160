# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: descarteslabs/common/proto/testing/testing.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0descarteslabs/common/proto/testing/testing.proto\x12\ntesting.v1\"\x1f\n\x07Request\x12\x14\n\x05value\x18\x01 \x01(\tR\x05value\" \n\x08Response\x12\x14\n\x05value\x18\x01 \x01(\tR\x05value2\x85\x02\n\x0bTestService\x12?\n\x0cStreamStream\x12\x13.testing.v1.Request\x1a\x14.testing.v1.Response\"\x00(\x01\x30\x01\x12<\n\x0bStreamUnary\x12\x13.testing.v1.Request\x1a\x14.testing.v1.Response\"\x00(\x01\x12<\n\x0bUnaryStream\x12\x13.testing.v1.Request\x1a\x14.testing.v1.Response\"\x00\x30\x01\x12\x39\n\nUnaryUnary\x12\x13.testing.v1.Request\x1a\x14.testing.v1.Response\"\x00\x62\x06proto3')



_REQUEST = DESCRIPTOR.message_types_by_name['Request']
_RESPONSE = DESCRIPTOR.message_types_by_name['Response']
Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'descarteslabs._dl_modules.common.proto.testing.testing_pb2'
  # @@protoc_insertion_point(class_scope:testing.v1.Request)
  })
_sym_db.RegisterMessage(Request)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'descarteslabs._dl_modules.common.proto.testing.testing_pb2'
  # @@protoc_insertion_point(class_scope:testing.v1.Response)
  })
_sym_db.RegisterMessage(Response)

_TESTSERVICE = DESCRIPTOR.services_by_name['TestService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST._serialized_start=64
  _REQUEST._serialized_end=95
  _RESPONSE._serialized_start=97
  _RESPONSE._serialized_end=129
  _TESTSERVICE._serialized_start=132
  _TESTSERVICE._serialized_end=393
# @@protoc_insertion_point(module_scope)
