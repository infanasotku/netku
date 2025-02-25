package service

import "github.com/infanasotku/netku/services/xray/contracts"

type XrayService struct {
	CachingClient *contracts.XrayCachingClient
}
