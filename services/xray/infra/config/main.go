package config

import (
	"fmt"

	"github.com/joho/godotenv"
)

func ConfigureEnvs() error {
	err := checkXrayEnvs()
	if err == nil {
		err = checkRedisEnvs()
	}

	if err != nil {
		err = godotenv.Overload()
		if err != nil {
			return fmt.Errorf("error while loading .env file: %v", err)
		}

		err = checkXrayEnvs()
		if err == nil {
			err = checkRedisEnvs()
		}
		if err != nil {
			return fmt.Errorf("error while reading env: %v", err)
		}
	}
	return nil
}
