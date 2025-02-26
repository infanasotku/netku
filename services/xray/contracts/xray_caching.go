package contracts

import "context"

type XrayInfo struct {
	XrayUUID string
	Running  bool
}

type XrayCachingClient interface {
	RefreshTTL(context context.Context) error
	SetXrayInfo(context context.Context, info *XrayInfo) error
}
