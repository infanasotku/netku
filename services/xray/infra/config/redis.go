package config

import (
	"errors"
	"os"
)

func checkRedisEnvs() error {
	_, ok := os.LookupEnv("REDIS_ADDR")
	if !ok {
		return errors.New("REDIS_ADDR not specified")
	}

	_, ok = os.LookupEnv("REDIS_SECRET")
	if !ok {
		return errors.New("REDIS_SECRET not specified")
	}

	return nil
}
