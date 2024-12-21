// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.5.1
// - protoc             v5.29.1
// source: protobuf/xray.proto

package gen

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.64.0 or later.
const _ = grpc.SupportPackageIsVersion9

const (
	Xray_RestartXray_FullMethodName = "/Xray/RestartXray"
)

// XrayClient is the client API for Xray service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type XrayClient interface {
	RestartXray(ctx context.Context, in *Null, opts ...grpc.CallOption) (*RestartResponse, error)
}

type xrayClient struct {
	cc grpc.ClientConnInterface
}

func NewXrayClient(cc grpc.ClientConnInterface) XrayClient {
	return &xrayClient{cc}
}

func (c *xrayClient) RestartXray(ctx context.Context, in *Null, opts ...grpc.CallOption) (*RestartResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(RestartResponse)
	err := c.cc.Invoke(ctx, Xray_RestartXray_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// XrayServer is the server API for Xray service.
// All implementations must embed UnimplementedXrayServer
// for forward compatibility.
type XrayServer interface {
	RestartXray(context.Context, *Null) (*RestartResponse, error)
	mustEmbedUnimplementedXrayServer()
}

// UnimplementedXrayServer must be embedded to have
// forward compatible implementations.
//
// NOTE: this should be embedded by value instead of pointer to avoid a nil
// pointer dereference when methods are called.
type UnimplementedXrayServer struct{}

func (UnimplementedXrayServer) RestartXray(context.Context, *Null) (*RestartResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method RestartXray not implemented")
}
func (UnimplementedXrayServer) mustEmbedUnimplementedXrayServer() {}
func (UnimplementedXrayServer) testEmbeddedByValue()              {}

// UnsafeXrayServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to XrayServer will
// result in compilation errors.
type UnsafeXrayServer interface {
	mustEmbedUnimplementedXrayServer()
}

func RegisterXrayServer(s grpc.ServiceRegistrar, srv XrayServer) {
	// If the following call pancis, it indicates UnimplementedXrayServer was
	// embedded by pointer and is nil.  This will cause panics if an
	// unimplemented method is ever invoked, so we test this at initialization
	// time to prevent it from happening at runtime later due to I/O.
	if t, ok := srv.(interface{ testEmbeddedByValue() }); ok {
		t.testEmbeddedByValue()
	}
	s.RegisterService(&Xray_ServiceDesc, srv)
}

func _Xray_RestartXray_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Null)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(XrayServer).RestartXray(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Xray_RestartXray_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(XrayServer).RestartXray(ctx, req.(*Null))
	}
	return interceptor(ctx, in, info, handler)
}

// Xray_ServiceDesc is the grpc.ServiceDesc for Xray service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Xray_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "Xray",
	HandlerType: (*XrayServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "RestartXray",
			Handler:    _Xray_RestartXray_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "protobuf/xray.proto",
}
