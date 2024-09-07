package main

import (
	"errors"
	"log"
	"os"
	"path"
	"path/filepath"
	"strings"

	"github.com/infanasotku/netku/services/xray/handler"
	godotenv "github.com/joho/godotenv"
	_ "github.com/xtls/xray-core/main/distro/all"
)

func ConfigureEnvs() {
	err := checkEnvs()
	if err != nil {
		err = godotenv.Overload()
		if err != nil {
			log.Fatal("Error loading .env file")
		}
		err = checkEnvs()
		if err != nil {
			log.Fatal("Error reading env: ", err)
		}
	}
}

func ConfigureServer(s *handler.Server) {
	config_path := path.Join(os.Getenv("XRAY_CONFIG_DIR"), "config.json")

	configFileBytes, err := os.ReadFile(config_path)

	if err != nil {
		log.Fatal("Failed to open config file: ", err)
	}

	configFile := string(configFileBytes)

	logDir, _ := filepath.Abs(os.Getenv("XRAY_LOG_DIR"))

	configFile = strings.Replace(configFile, "example.com", os.Getenv("XRAY_FALLBACK"), 1)        // Fallback
	configFile = strings.Replace(configFile, "a_example.log", path.Join(logDir, "access.log"), 1) // Access log
	configFile = strings.Replace(configFile, "e_example.log", path.Join(logDir, "access.log"), 1) // Error log
	configFile = strings.Replace(configFile, "example.crt", os.Getenv("SSL_CERTFILE"), 1)         // Fallback
	configFile = strings.Replace(configFile, "example.key", os.Getenv("SSL_KEYFILE"), 1)          // Fallback

	err = s.LoadConfig(strings.NewReader(configFile))

	if err != nil {
		log.Fatal("Failed to load config file: ", err)
	}
}

func checkEnvs() error {
	_, ok := os.LookupEnv("XRAY_PORT")
	if !ok {
		return errors.New("XRAY_PORT not specified")
	}

	_, ok = os.LookupEnv("XRAY_CONFIG_DIR")
	if !ok {
		return errors.New("XRAY_CONFIG_DIR not specified")
	}

	_, ok = os.LookupEnv("XRAY_LOG_DIR")
	if !ok {
		return errors.New("XRAY_LOG_DIR not specified")
	}

	_, ok = os.LookupEnv("SSL_KEYFILE")
	if !ok {
		return errors.New("SSL_KEYFILE not specified")
	}

	_, ok = os.LookupEnv("SSL_CERTFILE")
	if !ok {
		return errors.New("SSL_CERTFILE not specified")
	}

	return nil
}
