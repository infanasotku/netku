package core

import (
	"context"

	"github.com/infanasotku/netku/services/booking/gen"
)

type Server struct {
	gen.UnimplementedBookingServer
}

// #region GRPC implementation
func (s *Server) Book(_ context.Context, r *gen.BookingRequest) (*gen.Null, error) {
	return &gen.Null{}, nil
}

func (s *Server) Unbook(_ context.Context, r *gen.BookingRequest) (*gen.Null, error) {
	return &gen.Null{}, nil
}

//#endregion
