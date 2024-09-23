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

func TestRun() {
	logger := initLogger()
	loop := createLoop("m.gerasimov1@g.nsu.ru", "426728qq", logger)
	loop.run()
	loop.wait()

	// go func() {
	// 	defer wg.Done()
	// 	runLoop("12346", "lovak4team48@gmail.com", "426728qq", logger)
	// }()
}
