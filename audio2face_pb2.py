# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: audio2face.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x61udio2face.proto\x12\naudio2face\",\n\x16PushAudioStreamRequest\x12\x12\n\naudio_data\x18\x01 \x01(\x0c\";\n\x17PushAudioStreamResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2j\n\nAudio2Face\x12\\\n\x0fPushAudioStream\x12\".audio2face.PushAudioStreamRequest\x1a#.audio2face.PushAudioStreamResponse(\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'audio2face_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PUSHAUDIOSTREAMREQUEST._serialized_start=32
  _PUSHAUDIOSTREAMREQUEST._serialized_end=76
  _PUSHAUDIOSTREAMRESPONSE._serialized_start=78
  _PUSHAUDIOSTREAMRESPONSE._serialized_end=137
  _AUDIO2FACE._serialized_start=139
  _AUDIO2FACE._serialized_end=245
# @@protoc_insertion_point(module_scope)