package core

import (
	"context"
	"errors"

	"github.com/charmbracelet/log"
	"github.com/infanasotku/netku/services/booking/gen"
)

type Server struct {
	gen.UnimplementedBookingServer
	loops  map[string]*Loop
	logger *log.Logger
}

// #region GRPC implementation
func (s *Server) RunBooking(_ context.Context, r *gen.BookingRequest) (*gen.Null, error) {
	loop, ok := s.loops[r.Email]
	if !ok {
		loop = createLoop(r.Email, r.Password, s.logger)
		s.loops[r.Email] = loop
	}

	if !loop.stopped() {
		return &gen.Null{}, errors.New("loop already ran")
	}

	loop.run()

	return &gen.Null{}, nil
}

func (s *Server) StopBooking(_ context.Context, r *gen.BookingRequest) (*gen.Null, error) {
	loop, ok := s.loops[r.Email]
	if !ok {
		return &gen.Null{}, errors.New("loop not exist")
	}

	if loop.stopped() {
		return &gen.Null{}, errors.New("loop already stopped")
	}

	loop.stop()
	loop.wait()

	return &gen.Null{}, nil
}

//#endregion

func CreateServer() *Server {
	return &Server{loops: make(map[string]*Loop), logger: initLogger()}
}