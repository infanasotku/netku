package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"path"
	"path/filepath"

	"github.com/infanasotku/netku/services/xray/infra/config"
	"github.com/infanasotku/netku/services/xray/infra/grpc"

	"github.com/sirupsen/logrus"
)

func main() {
	logrusLogger := logrus.New()

	err := config.ConfigureEnvs()

	if err != nil {
		logrusLogger.Fatalf("Failed to configure envs: %v", err)
	}

	serve(logrusLogger)
}

func serve(logger *logrus.Logger) {
	port := os.Getenv("GPRC_PORT")

	lis, err := net.Listen("tcp", fmt.Sprintf(":%s", port))
	if err != nil {
		log.Fatalf("Failed to listen on port %s: %v", port, err)
	}

	logDir, _ := filepath.Abs(os.Getenv("XRAY_LOG_DIR"))
	xrayConfig := &grpc.XrayConfig{
		ConfigFile:      path.Join(os.Getenv("XRAY_CONFIG_DIR"), "config.json"),
		LogDirPath:      logDir,
		XrayFallback:    os.Getenv("XRAY_FALLBACK"),
		SSLCertfilePath: os.Getenv("SSL_CERTFILE"),
		SSLKeyFilePath:  os.Getenv("SSL_KEYFILE"),
	}
	grpcServer, err := grpc.CreateGPRCServer(logger, true)
	if err != nil {
		log.Fatalf("Failed to create grpc server: %v", err)
	}
	grpc.BindXrayServer(grpcServer, xrayConfig)
	grpc.BindHealthCheck(grpcServer)

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("Failed to serve gRPC server over port %s: %v", port, err)
	}
}
