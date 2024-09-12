// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.5.1
// - protoc             v5.27.3
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
	XrayService_RestartXray_FullMethodName = "/xray_gen.XrayService/RestartXray"
)

// XrayServiceClient is the client API for XrayService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type XrayServiceClient interface {
	RestartXray(ctx context.Context, in *Null, opts ...grpc.CallOption) (*RestartResponse, error)
}

type xrayServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewXrayServiceClient(cc grpc.ClientConnInterface) XrayServiceClient {
	return &xrayServiceClient{cc}
}

func (c *xrayServiceClient) RestartXray(ctx context.Context, in *Null, opts ...grpc.CallOption) (*RestartResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(RestartResponse)
	err := c.cc.Invoke(ctx, XrayService_RestartXray_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// XrayServiceServer is the server API for XrayService service.
// All implementations must embed UnimplementedXrayServiceServer
// for forward compatibility.
type XrayServiceServer interface {
	RestartXray(context.Context, *Null) (*RestartResponse, error)
	mustEmbedUnimplementedXrayServiceServer()
}

// UnimplementedXrayServiceServer must be embedded to have
// forward compatible implementations.
//
// NOTE: this should be embedded by value instead of pointer to avoid a nil
// pointer dereference when methods are called.
type UnimplementedXrayServiceServer struct{}

func (UnimplementedXrayServiceServer) RestartXray(context.Context, *Null) (*RestartResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method RestartXray not implemented")
}
func (UnimplementedXrayServiceServer) mustEmbedUnimplementedXrayServiceServer() {}
func (UnimplementedXrayServiceServer) testEmbeddedByValue()                     {}

// UnsafeXrayServiceServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to XrayServiceServer will
// result in compilation errors.
type UnsafeXrayServiceServer interface {
	mustEmbedUnimplementedXrayServiceServer()
}

func RegisterXrayServiceServer(s grpc.ServiceRegistrar, srv XrayServiceServer) {
	// If the following call pancis, it indicates UnimplementedXrayServiceServer was
	// embedded by pointer and is nil.  This will cause panics if an
	// unimplemented method is ever invoked, so we test this at initialization
	// time to prevent it from happening at runtime later due to I/O.
	if t, ok := srv.(interface{ testEmbeddedByValue() }); ok {
		t.testEmbeddedByValue()
	}
	s.RegisterService(&XrayService_ServiceDesc, srv)
}

func _XrayService_RestartXray_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Null)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(XrayServiceServer).RestartXray(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: XrayService_RestartXray_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(XrayServiceServer).RestartXray(ctx, req.(*Null))
	}
	return interceptor(ctx, in, info, handler)
}

// XrayService_ServiceDesc is the grpc.ServiceDesc for XrayService service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var XrayService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "xray_gen.XrayService",
	HandlerType: (*XrayServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "RestartXray",
			Handler:    _XrayService_RestartXray_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "protobuf/xray.proto",
}
