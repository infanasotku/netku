package grpc

import (
	"fmt"
	"os"
	"path"
	"strings"
)

type XrayConfig struct {
	ConfigFile      string
	LogDirPath      string
	XrayFallback    string
	SSLCertfilePath string
	SSLKeyFilePath  string
}

func configureXrayServer(server *XrayServer, config *XrayConfig) error {
	configFileBytes, err := os.ReadFile(config.ConfigFile)

	if err != nil {
		return fmt.Errorf("failed to open config file: %v", err)
	}

	configFile := string(configFileBytes)

	logDir := config.LogDirPath

	configFile = strings.Replace(configFile, "example.com", config.XrayFallback, 1)               // Fallback
	configFile = strings.Replace(configFile, "a_example.log", path.Join(logDir, "access.log"), 1) // Access log
	configFile = strings.Replace(configFile, "e_example.log", path.Join(logDir, "error.log"), 1)  // Error log
	configFile = strings.Replace(configFile, "example.crt", config.SSLCertfilePath, 1)            // Fallback
	configFile = strings.Replace(configFile, "example.key", config.SSLKeyFilePath, 1)             // Fallback

	err = server.LoadConfig(strings.NewReader(configFile))

	if err != nil {
		return fmt.Errorf("failed to load config file: %v", err)
	}

	return nil
}
