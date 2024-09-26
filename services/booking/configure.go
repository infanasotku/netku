package main

import (
	"errors"
	"log"
	"os"

	godotenv "github.com/joho/godotenv"
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

func checkEnvs() error {
	_, ok := os.LookupEnv("SSL_KEYFILE")
	if !ok {
		return errors.New("SSL_KEYFILE not specified")
	}

	_, ok = os.LookupEnv("SSL_CERTFILE")
	if !ok {
		return errors.New("SSL_CERTFILE not specified")
	}

	_, ok = os.LookupEnv("BOOKING_PORT")
	if !ok {
		return errors.New("BOOKING_PORT not specified")
	}

	return nil
}
