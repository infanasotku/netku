package handler

import (
	"log"

	context "golang.org/x/net/context"
)

type Server struct {}

func (Server) RestartXray(context.Context, *Null) (*RestartResponse, error) {
	log.Printf("Calls recieved!");
	return &RestartResponse{Uuid: "test-uuid"}, nil
}

func (Server) mustEmbedUnimplementedHandlerServiceServer() {}