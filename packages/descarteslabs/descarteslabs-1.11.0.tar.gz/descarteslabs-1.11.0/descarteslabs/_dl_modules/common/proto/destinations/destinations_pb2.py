# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: descarteslabs/common/proto/destinations/destinations.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n:descarteslabs/common/proto/destinations/destinations.proto\x12\x17\x64\x65scarteslabs.workflows\"\x9f\x02\n\x0b\x44\x65stination\x12=\n\x08\x64ownload\x18\x01 \x01(\x0b\x32!.descarteslabs.workflows.DownloadR\x08\x64ownload\x12\x34\n\x05\x65mail\x18\x02 \x01(\x0b\x32\x1e.descarteslabs.workflows.EmailR\x05\x65mail\x12:\n\x07\x63\x61talog\x18\x03 \x01(\x0b\x32 .descarteslabs.workflows.CatalogR\x07\x63\x61talog\x12!\n\x0chas_download\x18\x14 \x01(\x08R\x0bhasDownload\x12\x1b\n\thas_email\x18\x15 \x01(\x08R\x08hasEmail\x12\x1f\n\x0bhas_catalog\x18\x17 \x01(\x08R\nhasCatalog\")\n\x08\x44ownload\x12\x1d\n\nresult_url\x18\x01 \x01(\tR\tresultUrl\"T\n\x05\x45mail\x12\x18\n\x07subject\x18\x01 \x01(\tR\x07subject\x12\x12\n\x04\x62ody\x18\x02 \x01(\tR\x04\x62ody\x12\x1d\n\nresult_url\x18\x03 \x01(\tR\tresultUrl\"\xb9\x02\n\x07\x43\x61talog\x12\x1c\n\toverwrite\x18\x01 \x01(\x08R\toverwrite\x12\x18\n\x07rescale\x18\x02 \x01(\x08R\x07rescale\x12!\n\x0c\x63hange_dtype\x18\x03 \x01(\x08R\x0b\x63hangeDtype\x12\x12\n\x04name\x18\n \x01(\tR\x04name\x12\x1d\n\nproduct_id\x18\x0b \x01(\tR\tproductId\x12]\n\x0f\x61ttributes_json\x18\r \x03(\x0b\x32\x34.descarteslabs.workflows.Catalog.AttributesJsonEntryR\x0e\x61ttributesJson\x1a\x41\n\x13\x41ttributesJsonEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x62\x06proto3')



_DESTINATION = DESCRIPTOR.message_types_by_name['Destination']
_DOWNLOAD = DESCRIPTOR.message_types_by_name['Download']
_EMAIL = DESCRIPTOR.message_types_by_name['Email']
_CATALOG = DESCRIPTOR.message_types_by_name['Catalog']
_CATALOG_ATTRIBUTESJSONENTRY = _CATALOG.nested_types_by_name['AttributesJsonEntry']
Destination = _reflection.GeneratedProtocolMessageType('Destination', (_message.Message,), {
  'DESCRIPTOR' : _DESTINATION,
  '__module__' : 'descarteslabs._dl_modules.common.proto.destinations.destinations_pb2'
  # @@protoc_insertion_point(class_scope:descarteslabs.workflows.Destination)
  })
_sym_db.RegisterMessage(Destination)

Download = _reflection.GeneratedProtocolMessageType('Download', (_message.Message,), {
  'DESCRIPTOR' : _DOWNLOAD,
  '__module__' : 'descarteslabs._dl_modules.common.proto.destinations.destinations_pb2'
  # @@protoc_insertion_point(class_scope:descarteslabs.workflows.Download)
  })
_sym_db.RegisterMessage(Download)

Email = _reflection.GeneratedProtocolMessageType('Email', (_message.Message,), {
  'DESCRIPTOR' : _EMAIL,
  '__module__' : 'descarteslabs._dl_modules.common.proto.destinations.destinations_pb2'
  # @@protoc_insertion_point(class_scope:descarteslabs.workflows.Email)
  })
_sym_db.RegisterMessage(Email)

Catalog = _reflection.GeneratedProtocolMessageType('Catalog', (_message.Message,), {

  'AttributesJsonEntry' : _reflection.GeneratedProtocolMessageType('AttributesJsonEntry', (_message.Message,), {
    'DESCRIPTOR' : _CATALOG_ATTRIBUTESJSONENTRY,
    '__module__' : 'descarteslabs._dl_modules.common.proto.destinations.destinations_pb2'
    # @@protoc_insertion_point(class_scope:descarteslabs.workflows.Catalog.AttributesJsonEntry)
    })
  ,
  'DESCRIPTOR' : _CATALOG,
  '__module__' : 'descarteslabs._dl_modules.common.proto.destinations.destinations_pb2'
  # @@protoc_insertion_point(class_scope:descarteslabs.workflows.Catalog)
  })
_sym_db.RegisterMessage(Catalog)
_sym_db.RegisterMessage(Catalog.AttributesJsonEntry)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CATALOG_ATTRIBUTESJSONENTRY._options = None
  _CATALOG_ATTRIBUTESJSONENTRY._serialized_options = b'8\001'
  _DESTINATION._serialized_start=88
  _DESTINATION._serialized_end=375
  _DOWNLOAD._serialized_start=377
  _DOWNLOAD._serialized_end=418
  _EMAIL._serialized_start=420
  _EMAIL._serialized_end=504
  _CATALOG._serialized_start=507
  _CATALOG._serialized_end=820
  _CATALOG_ATTRIBUTESJSONENTRY._serialized_start=755
  _CATALOG_ATTRIBUTESJSONENTRY._serialized_end=820
# @@protoc_insertion_point(module_scope)
