package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"os"

	"github.com/infanasotku/netku/services/booking/core"
	"github.com/infanasotku/netku/services/booking/gen"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/health"
	healthgrpc "google.golang.org/grpc/health/grpc_health_v1"
	"google.golang.org/grpc/reflection"
)

func main() {
	ConfigureEnvs()

	// Health check mode.
	if len(os.Args) > 1 && os.Args[1] == "--greet" {
		os.Exit(greet())
	}

	serve()
}

func getCredentials(clientCredentials bool) (credentials.TransportCredentials, error) {
	keyfile := os.Getenv("SSL_KEYFILE")
	certfile := os.Getenv("SSL_CERTFILE")

	if clientCredentials {
		return credentials.NewClientTLSFromFile(certfile, keyfile)
	}
	return credentials.NewServerTLSFromFile(certfile, keyfile)
}

func greet() int {
	port := os.Getenv("BOOKING_PORT")

	creds, err := getCredentials(true)
	if err != nil {
		return 1
	}

	conn, err := grpc.NewClient(fmt.Sprintf("localhost:%s", port), grpc.WithTransportCredentials(creds))
	if err != nil {
		return 1
	}
	defer conn.Close()

	checker := healthgrpc.NewHealthClient(conn)
	_, err = checker.Check(context.Background(), &healthgrpc.HealthCheckRequest{Service: "booking"})

	if err != nil {
		return 1
	}
	return 0
}

func serve() {
	port := os.Getenv("BOOKING_PORT")

	lis, err := net.Listen("tcp", fmt.Sprintf(":%s", port))
	if err != nil {
		log.Fatalf("Failed to listen on port %s: %v", port, err)
	}

	creds, err := getCredentials(false)
	if err != nil {
		log.Fatalf("Failed to load credentials: %v", err)
	}

	grpcServer := grpc.NewServer(grpc.Creds(creds))

	reflection.Register(grpcServer)
	healthcheck := health.NewServer()
	healthgrpc.RegisterHealthServer(grpcServer, healthcheck)

	server := core.CreateServer()
	defer core.CloseServer(server)
	gen.RegisterBookingServer(grpcServer, server)
	healthcheck.SetServingStatus("booking", healthgrpc.HealthCheckResponse_SERVING)

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve gRPC server over port %s: %v", port, err)
	}
}
