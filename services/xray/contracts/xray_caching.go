package contracts

import (
	"context"
	"errors"
)

type XrayInfo struct {
	XrayUUID string
	Running  bool
	GRPCAddr string
}

var ErrEngineHashNotFound = errors.New("engine hash does not exist")

type XrayCachingClient interface {
	RefreshTTL(context context.Context) error
	SetXrayInfo(context context.Context, info *XrayInfo) error
	CreateWithTTL(context context.Context, extraFields ...interface{}) error
}
