package contracts

import "context"

type XrayInfo struct {
	XrayUUID string
	Running  bool
	GRPCAddr string
}

type XrayCachingClient interface {
	RefreshTTL(context context.Context) error
	SetXrayInfo(context context.Context, info *XrayInfo) error
	CreateWithTTL(context context.Context, extraFields ...interface{}) error
}
