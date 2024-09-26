package core

import (
	"context"
	"errors"

	"github.com/charmbracelet/log"
	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/launcher"
	"github.com/infanasotku/netku/services/booking/gen"
)

type Server struct {
	gen.UnimplementedBookingServer
	loops   map[string]*Loop
	logger  *log.Logger
	browser *rod.Browser
}

// #region GRPC implementation
func (s *Server) RunBooking(_ context.Context, r *gen.BookingRequest) (*gen.BookingResponse, error) {
	loop, ok := s.loops[r.Email]
	if !ok {
		loop = createLoop(r.Email, r.Password, s.logger, s.browser)
		s.loops[r.Email] = loop
	} else if !loop.stopped() {
		return &gen.BookingResponse{Booked: true}, errors.New("loop already ran")
	}

	loop.run()

	return &gen.BookingResponse{Booked: true}, nil
}

func (s *Server) StopBooking(_ context.Context, r *gen.BookingRequest) (*gen.BookingResponse, error) {
	loop, ok := s.loops[r.Email]
	if !ok {
		return &gen.BookingResponse{Booked: false}, errors.New("loop not exist")
	}

	if loop.stopped() {
		return &gen.BookingResponse{Booked: false}, errors.New("loop already stopped")
	}

	loop.stop()
	loop.wait()

	return &gen.BookingResponse{Booked: false}, nil
}

func (s *Server) Booked(_ context.Context, r *gen.BookingRequest) (*gen.BookingResponse, error) {
	loop, ok := s.loops[r.Email]
	if !ok || loop.stopped() {
		return &gen.BookingResponse{Booked: false}, nil
	}
	return &gen.BookingResponse{Booked: true}, nil
}

//#endregion

func CreateServer() *Server {
	url := launcher.New().Headless(true).NoSandbox(true).Set("--disable-gpu").MustLaunch()
	browser := rod.New().ControlURL(url).MustConnect()

	return &Server{loops: make(map[string]*Loop), logger: initLogger(), browser: browser}
}

func CloseServer(s *Server) {
	s.browser.MustClose()
}
