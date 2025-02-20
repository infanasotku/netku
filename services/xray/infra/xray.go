package infra

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"log"
	"regexp"

	"github.com/infanasotku/netku/services/xray/gen"
	"github.com/xtls/xray-core/core"
)

type Server struct {
	gen.UnimplementedXrayServer
	xrayServer core.Server
	xrayConfig *core.Config
}

func IsValidUUID(uuid string) bool {
	r := regexp.MustCompile("^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[8|9|aA|bB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$")
	return r.MatchString(uuid)
}

func (s *Server) RestartXray(_ context.Context, req *gen.RestartRequest) (*gen.RestartResponse, error) {
	fmt.Println(req.Uuid)
	if !IsValidUUID((req.Uuid)) {
		return nil, errors.New("specified uuid not valid")
	}

	if s.xrayServer != nil {
		s.xrayServer.Close()
	}

	convertedId := req.Uuid
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
