package main

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"log"

	"github.com/infanasotku/netku/services/xray/gen"
	"github.com/xtls/xray-core/common/uuid"
	"github.com/xtls/xray-core/core"
)

type Server struct {
	gen.UnimplementedXrayServer
	xrayServer core.Server
	xrayConfig *core.Config
}

func (s *Server) RestartXray(context.Context, *gen.Null) (*gen.RestartResponse, error) {
	if s.xrayServer != nil {
		s.xrayServer.Close()
	}

	id := uuid.New()
	convertedId := id.String()
	idStart := bytes.IndexByte(s.xrayConfig.Inbound[0].ProxySettings.Value, '$') + 1
	for i := 0; i < len(convertedId); i++ {
		s.xrayConfig.Inbound[0].ProxySettings.Value[idStart+i] = convertedId[i]
	}

	server, err := core.New(s.xrayConfig)
	if err != nil {
		log.Fatal("Failed to create server: ", err)
	}

	s.xrayServer = server
	err = s.xrayServer.Start()

	if err != nil {
		log.Fatal("Failed to run server: ", err)
	}

	return &gen.RestartResponse{Uuid: convertedId}, nil
}

// Loads and saves xray config to server.
func (s *Server) LoadConfig(configFile io.Reader) error {
	c, err := core.LoadConfig("json", configFile)
	if err != nil {
		return errors.New(fmt.Sprintln("Failed to load config file: ", err))
	}

	s.xrayConfig = c

	return nil
}
