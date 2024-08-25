package main

import (
	"log"
	"net"

	"google.golang.org/grpc"

	"github.com/infanasotku/netku/services/xray/handler"
)

func main() {
	const port int = 9000

	lis, err := net.Listen("tcp", ":9000")
	if err != nil {
		log.Fatalf("Failde to listen on port %o: %v", port, err)
	}

	grpcServer := grpc.NewServer()

	handler.RegisterHandlerServiceServer(grpcServer, handler.Server{})

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve gRPC server over port %o: %v", port, err)
	}
}