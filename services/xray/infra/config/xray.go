package config

import (
	"errors"
	"os"
)

func checkXrayEnvs() error {
	_, ok := os.LookupEnv("GPRC_PORT")
	if !ok {
		return errors.New("GPRC_PORT not specified")
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
