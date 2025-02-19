// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.36.5
// 	protoc        v5.29.3
// source: proto/xray.proto

package gen

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
	unsafe "unsafe"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type RestartResponse struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Uuid          string                 `protobuf:"bytes,1,opt,name=uuid,proto3" json:"uuid,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *RestartResponse) Reset() {
	*x = RestartResponse{}
	mi := &file_proto_xray_proto_msgTypes[0]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *RestartResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*RestartResponse) ProtoMessage() {}

func (x *RestartResponse) ProtoReflect() protoreflect.Message {
	mi := &file_proto_xray_proto_msgTypes[0]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use RestartResponse.ProtoReflect.Descriptor instead.
func (*RestartResponse) Descriptor() ([]byte, []int) {
	return file_proto_xray_proto_rawDescGZIP(), []int{0}
}

func (x *RestartResponse) GetUuid() string {
	if x != nil {
		return x.Uuid
	}
	return ""
}

type RestartRequest struct {
	state         protoimpl.MessageState `protogen:"open.v1"`
	Uuid          string                 `protobuf:"bytes,1,opt,name=uuid,proto3" json:"uuid,omitempty"`
	unknownFields protoimpl.UnknownFields
	sizeCache     protoimpl.SizeCache
}

func (x *RestartRequest) Reset() {
	*x = RestartRequest{}
	mi := &file_proto_xray_proto_msgTypes[1]
	ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
	ms.StoreMessageInfo(mi)
}

func (x *RestartRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*RestartRequest) ProtoMessage() {}

func (x *RestartRequest) ProtoReflect() protoreflect.Message {
	mi := &file_proto_xray_proto_msgTypes[1]
	if x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use RestartRequest.ProtoReflect.Descriptor instead.
func (*RestartRequest) Descriptor() ([]byte, []int) {
	return file_proto_xray_proto_rawDescGZIP(), []int{1}
}

func (x *RestartRequest) GetUuid() string {
	if x != nil {
		return x.Uuid
	}
	return ""
}

var File_proto_xray_proto protoreflect.FileDescriptor

var file_proto_xray_proto_rawDesc = string([]byte{
	0x0a, 0x10, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x2f, 0x78, 0x72, 0x61, 0x79, 0x2e, 0x70, 0x72, 0x6f,
	0x74, 0x6f, 0x22, 0x25, 0x0a, 0x0f, 0x52, 0x65, 0x73, 0x74, 0x61, 0x72, 0x74, 0x52, 0x65, 0x73,
	0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x12, 0x0a, 0x04, 0x75, 0x75, 0x69, 0x64, 0x18, 0x01, 0x20,
	0x01, 0x28, 0x09, 0x52, 0x04, 0x75, 0x75, 0x69, 0x64, 0x22, 0x24, 0x0a, 0x0e, 0x52, 0x65, 0x73,
	0x74, 0x61, 0x72, 0x74, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x12, 0x0a, 0x04, 0x75,
	0x75, 0x69, 0x64, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x75, 0x75, 0x69, 0x64, 0x32,
	0x3a, 0x0a, 0x04, 0x58, 0x72, 0x61, 0x79, 0x12, 0x32, 0x0a, 0x0b, 0x52, 0x65, 0x73, 0x74, 0x61,
	0x72, 0x74, 0x58, 0x72, 0x61, 0x79, 0x12, 0x0f, 0x2e, 0x52, 0x65, 0x73, 0x74, 0x61, 0x72, 0x74,
	0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x10, 0x2e, 0x52, 0x65, 0x73, 0x74, 0x61, 0x72,
	0x74, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x22, 0x00, 0x62, 0x06, 0x70, 0x72, 0x6f,
	0x74, 0x6f, 0x33,
})

var (
	file_proto_xray_proto_rawDescOnce sync.Once
	file_proto_xray_proto_rawDescData []byte
)

func file_proto_xray_proto_rawDescGZIP() []byte {
	file_proto_xray_proto_rawDescOnce.Do(func() {
		file_proto_xray_proto_rawDescData = protoimpl.X.CompressGZIP(unsafe.Slice(unsafe.StringData(file_proto_xray_proto_rawDesc), len(file_proto_xray_proto_rawDesc)))
	})
	return file_proto_xray_proto_rawDescData
}

var file_proto_xray_proto_msgTypes = make([]protoimpl.MessageInfo, 2)
var file_proto_xray_proto_goTypes = []any{
	(*RestartResponse)(nil), // 0: RestartResponse
	(*RestartRequest)(nil),  // 1: RestartRequest
}
var file_proto_xray_proto_depIdxs = []int32{
	1, // 0: Xray.RestartXray:input_type -> RestartRequest
	0, // 1: Xray.RestartXray:output_type -> RestartResponse
	1, // [1:2] is the sub-list for method output_type
	0, // [0:1] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_proto_xray_proto_init() }
func file_proto_xray_proto_init() {
	if File_proto_xray_proto != nil {
		return
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: unsafe.Slice(unsafe.StringData(file_proto_xray_proto_rawDesc), len(file_proto_xray_proto_rawDesc)),
			NumEnums:      0,
			NumMessages:   2,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_proto_xray_proto_goTypes,
		DependencyIndexes: file_proto_xray_proto_depIdxs,
		MessageInfos:      file_proto_xray_proto_msgTypes,
	}.Build()
	File_proto_xray_proto = out.File
	file_proto_xray_proto_goTypes = nil
	file_proto_xray_proto_depIdxs = nil
}
