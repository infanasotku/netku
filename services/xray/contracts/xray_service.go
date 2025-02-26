package contracts

import "context"

type XrayService interface {
	RefreshTTL(context context.Context) error
	RestartEngine(context context.Context, uuid string) error
}
