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
	Booking_Book_FullMethodName   = "/booking.Booking/Book"
	Booking_Unbook_FullMethodName = "/booking.Booking/Unbook"
)

// BookingClient is the client API for Booking service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type BookingClient interface {
	Book(ctx context.Context, in *BookingRequest, opts ...grpc.CallOption) (*Null, error)
	Unbook(ctx context.Context, in *BookingRequest, opts ...grpc.CallOption) (*Null, error)
}

type bookingClient struct {
	cc grpc.ClientConnInterface
}

func NewBookingClient(cc grpc.ClientConnInterface) BookingClient {
	return &bookingClient{cc}
}

func (c *bookingClient) Book(ctx context.Context, in *BookingRequest, opts ...grpc.CallOption) (*Null, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(Null)
	err := c.cc.Invoke(ctx, Booking_Book_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *bookingClient) Unbook(ctx context.Context, in *BookingRequest, opts ...grpc.CallOption) (*Null, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(Null)
	err := c.cc.Invoke(ctx, Booking_Unbook_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// BookingServer is the server API for Booking service.
// All implementations must embed UnimplementedBookingServer
// for forward compatibility.
type BookingServer interface {
	Book(context.Context, *BookingRequest) (*Null, error)
	Unbook(context.Context, *BookingRequest) (*Null, error)
	mustEmbedUnimplementedBookingServer()
}

// UnimplementedBookingServer must be embedded to have
// forward compatible implementations.
//
// NOTE: this should be embedded by value instead of pointer to avoid a nil
// pointer dereference when methods are called.
type UnimplementedBookingServer struct{}

func (UnimplementedBookingServer) Book(context.Context, *BookingRequest) (*Null, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Book not implemented")
}
func (UnimplementedBookingServer) Unbook(context.Context, *BookingRequest) (*Null, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Unbook not implemented")
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

func _Booking_Book_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BookingRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BookingServer).Book(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Booking_Book_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BookingServer).Book(ctx, req.(*BookingRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Booking_Unbook_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BookingRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BookingServer).Unbook(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Booking_Unbook_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BookingServer).Unbook(ctx, req.(*BookingRequest))
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
			MethodName: "Book",
			Handler:    _Booking_Book_Handler,
		},
		{
			MethodName: "Unbook",
			Handler:    _Booking_Unbook_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "protobuf/booking.proto",
}
