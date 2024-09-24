// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.5.1
// - protoc             v5.27.3
// source: protobuf/booking.proto

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
	Booking_RunBooking_FullMethodName  = "/booking.Booking/RunBooking"
	Booking_StopBooking_FullMethodName = "/booking.Booking/StopBooking"
)

// BookingClient is the client API for Booking service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type BookingClient interface {
	RunBooking(ctx context.Context, in *BookingRequest, opts ...grpc.CallOption) (*Null, error)
	StopBooking(ctx context.Context, in *BookingRequest, opts ...grpc.CallOption) (*Null, error)
}

type bookingClient struct {
	cc grpc.ClientConnInterface
}

func NewBookingClient(cc grpc.ClientConnInterface) BookingClient {
	return &bookingClient{cc}
}

func (c *bookingClient) RunBooking(ctx context.Context, in *BookingRequest, opts ...grpc.CallOption) (*Null, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(Null)
	err := c.cc.Invoke(ctx, Booking_RunBooking_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *bookingClient) StopBooking(ctx context.Context, in *BookingRequest, opts ...grpc.CallOption) (*Null, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(Null)
	err := c.cc.Invoke(ctx, Booking_StopBooking_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// BookingServer is the server API for Booking service.
// All implementations must embed UnimplementedBookingServer
// for forward compatibility.
type BookingServer interface {
	RunBooking(context.Context, *BookingRequest) (*Null, error)
	StopBooking(context.Context, *BookingRequest) (*Null, error)
	mustEmbedUnimplementedBookingServer()
}

// UnimplementedBookingServer must be embedded to have
// forward compatible implementations.
//
// NOTE: this should be embedded by value instead of pointer to avoid a nil
// pointer dereference when methods are called.
type UnimplementedBookingServer struct{}

func (UnimplementedBookingServer) RunBooking(context.Context, *BookingRequest) (*Null, error) {
	return nil, status.Errorf(codes.Unimplemented, "method RunBooking not implemented")
}
func (UnimplementedBookingServer) StopBooking(context.Context, *BookingRequest) (*Null, error) {
	return nil, status.Errorf(codes.Unimplemented, "method StopBooking not implemented")
}
func (UnimplementedBookingServer) mustEmbedUnimplementedBookingServer() {}
func (UnimplementedBookingServer) testEmbeddedByValue()                 {}

// UnsafeBookingServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to BookingServer will
// result in compilation errors.
type UnsafeBookingServer interface {
	mustEmbedUnimplementedBookingServer()
}

func RegisterBookingServer(s grpc.ServiceRegistrar, srv BookingServer) {
	// If the following call pancis, it indicates UnimplementedBookingServer was
	// embedded by pointer and is nil.  This will cause panics if an
	// unimplemented method is ever invoked, so we test this at initialization
	// time to prevent it from happening at runtime later due to I/O.
	if t, ok := srv.(interface{ testEmbeddedByValue() }); ok {
		t.testEmbeddedByValue()
	}
	s.RegisterService(&Booking_ServiceDesc, srv)
}

func _Booking_RunBooking_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BookingRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BookingServer).RunBooking(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Booking_RunBooking_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BookingServer).RunBooking(ctx, req.(*BookingRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Booking_StopBooking_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BookingRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BookingServer).StopBooking(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Booking_StopBooking_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BookingServer).StopBooking(ctx, req.(*BookingRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// Booking_ServiceDesc is the grpc.ServiceDesc for Booking service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Booking_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "booking.Booking",
	HandlerType: (*BookingServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "RunBooking",
			Handler:    _Booking_RunBooking_Handler,
		},
		{
			MethodName: "StopBooking",
			Handler:    _Booking_StopBooking_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "protobuf/booking.proto",
}
