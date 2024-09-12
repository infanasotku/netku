package main

import (
	"fmt"
	"log"
	"net"
	"os"

	"github.com/infanasotku/netku/services/xray/gen"
	"google.golang.org/grpc"
)

func main() {
	ConfigureEnvs()
	port := os.Getenv("XRAY_PORT")

	lis, err := net.Listen("tcp", fmt.Sprintf(":%s", port))
	if err != nil {
		log.Fatalf("Failed to listen on port %s: %v", port, err)
	}

	grpcServer := grpc.NewServer()

	server := Server{}
	ConfigureServer(&server)
	gen.RegisterXrayServiceServer(grpcServer, &server)

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve gRPC server over port %s: %v", port, err)
	}
}
