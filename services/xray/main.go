package main

import (
	"fmt"
	"log"
	"net"
	"os"

	"google.golang.org/grpc"

	"github.com/infanasotku/netku/services/xray/handler"
)

func main() {
	ConfigureEnvs()
	port := os.Getenv("XRAY_PORT")

	lis, err := net.Listen("tcp", fmt.Sprintf(":%s", port))
	if err != nil {
		log.Fatalf("Failde to listen on port %s: %v", port, err)
	}

	grpcServer := grpc.NewServer()

	server := handler.Server{}
	ConfigureServer(&server)

	handler.RegisterHandlerServiceServer(grpcServer, &server)

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve gRPC server over port %s: %v", port, err)
	}
}
