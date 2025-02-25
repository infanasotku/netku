package grpc

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"log"
	"regexp"

	"github.com/infanasotku/netku/services/xray/infra/grpc/gen"
	"github.com/xtls/xray-core/core"
)

type XrayServer struct {
	gen.UnimplementedXrayServer
	xrayServer *core.Instance
	xrayConfig *core.Config
	uuid       string
}

func IsValidUUID(uuid string) bool {
	r := regexp.MustCompile("^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[8|9|aA|bB][a-fA-F0-9]{3}-[a-fA-F0-9]{12}$")
	return r.MatchString(uuid)
}

func (s *XrayServer) RestartXray(_ context.Context, req *gen.XrayInfo) (*gen.XrayInfo, error) {
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
	s.uuid = req.Uuid
	err = s.xrayServer.Start()

	if err != nil {
		log.Fatal("Failed to run server: ", err)
	}

	return &gen.XrayInfo{Uuid: convertedId}, nil
}

func (s *XrayServer) CheckXrayHealth(context.Context, *gen.Null) (*gen.XrayFullInfo, error) {
	return &gen.XrayFullInfo{Running: s.xrayServer != nil, Uuid: s.uuid}, nil
}

// Loads and saves xray config to server.
func (s *XrayServer) LoadConfig(configFile io.Reader) error {
	c, err := core.LoadConfig("json", configFile)
	if err != nil {
		return errors.New(fmt.Sprintln("Failed to load config file: ", err))
	}

	s.xrayConfig = c
	s.uuid = ""

	return nil
}
