package main

import (
	"fmt"
	"log"
	"net"
	"os"

	"github.com/infanasotku/netku/services/xray/gen"
	"google.golang.org/grpc"
	"google.golang.org/grpc/health"
	healthgrpc "google.golang.org/grpc/health/grpc_health_v1"
)

func main() {
	ConfigureEnvs()
	port := os.Getenv("XRAY_PORT")

	lis, err := net.Listen("tcp", fmt.Sprintf(":%s", port))
	if err != nil {
		log.Fatalf("Failed to listen on port %s: %v", port, err)
	}

	grpcServer := grpc.NewServer()

	healthcheck := health.NewServer()
	healthgrpc.RegisterHealthServer(grpcServer, healthcheck)

	server := Server{}
	ConfigureServer(&server)
	gen.RegisterXrayServer(grpcServer, &server)
	healthcheck.SetServingStatus("xray", healthgrpc.HealthCheckResponse_SERVING)

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve gRPC server over port %s: %v", port, err)
	}
}
