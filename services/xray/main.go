package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"os"

	"github.com/infanasotku/netku/services/xray/gen"
	"github.com/infanasotku/netku/services/xray/infra"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/health"
	healthgrpc "google.golang.org/grpc/health/grpc_health_v1"
	"google.golang.org/grpc/reflection"

	grpc_logrus "github.com/grpc-ecosystem/go-grpc-middleware/logging/logrus"
	grpc_ctxtags "github.com/grpc-ecosystem/go-grpc-middleware/tags"
	"github.com/sirupsen/logrus"
)

var (
	logrusLogger = logrus.New()
	customFunc   = func(code codes.Code) logrus.Level {
		if code == codes.OK {
			return logrus.InfoLevel
		}
		return logrus.ErrorLevel
	}
)

func main() {
	infra.ConfigureEnvs()

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
		return credentials.NewClientTLSFromFile(certfile, "")
	}
	return credentials.NewServerTLSFromFile(certfile, keyfile)
}

func greet() int {
	port := os.Getenv("XRAY_PORT")

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
	_, err = checker.Check(context.Background(), &healthgrpc.HealthCheckRequest{Service: "xray"})

	if err != nil {
		return 1
	}
	return 0
}

func serve() {
	port := os.Getenv("XRAY_PORT")

	lis, err := net.Listen("tcp", fmt.Sprintf(":%s", port))
	if err != nil {
		log.Fatalf("Failed to listen on port %s: %v", port, err)
	}

	creds, err := getCredentials(false)
	if err != nil {
		log.Fatalf("Failed to load credentials: %v", err)
	}

	logrusEntry := logrus.NewEntry(logrusLogger)
	opts := []grpc_logrus.Option{
		grpc_logrus.WithLevels(customFunc),
	}
	grpc_logrus.ReplaceGrpcLogger(logrusEntry)

	grpcServer := grpc.NewServer(grpc.Creds(creds), grpc.ChainUnaryInterceptor(grpc_ctxtags.UnaryServerInterceptor(grpc_ctxtags.WithFieldExtractor(grpc_ctxtags.CodeGenRequestFieldExtractor)),
		grpc_logrus.UnaryServerInterceptor(logrusEntry, opts...)),
		grpc.ChainStreamInterceptor(
			grpc_ctxtags.StreamServerInterceptor(grpc_ctxtags.WithFieldExtractor(grpc_ctxtags.CodeGenRequestFieldExtractor)),
			grpc_logrus.StreamServerInterceptor(logrusEntry, opts...),
		))

	reflection.Register(grpcServer)
	healthcheck := health.NewServer()
	healthgrpc.RegisterHealthServer(grpcServer, healthcheck)

	server := infra.Server{}
	infra.ConfigureServer(&server)
	gen.RegisterXrayServer(grpcServer, &server)
	healthcheck.SetServingStatus("xray", healthgrpc.HealthCheckResponse_SERVING)

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve gRPC server over port %s: %v", port, err)
	}
}
