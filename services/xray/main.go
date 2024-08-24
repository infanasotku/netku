package main

import (
	"log"
	"net"

	"google.golang.org/grpc"
)

func main() {
	const port int = 9000

	lis, err := net.Listen("tcp", ":9000")
	if err != nil {
		log.Fatalf("Failde to listen on port %o: %v", port, err)
	}

	grpcServer := grpc.NewServer()

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve gRPC server over port %o: %v", port, err)
	}
}