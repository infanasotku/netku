package caching

import (
	"context"
	"fmt"
	"time"

	"github.com/infanasotku/netku/services/xray/contracts"
	"github.com/redis/go-redis/v9"
)

type RedisXrayCachingClient struct {
	client   *redis.Client
	infoTTL  time.Duration
	engineID string
	location *time.Location
}

func (c *RedisXrayCachingClient) RefreshTTL(context context.Context) error {
	hashKey := "engines:" + c.engineID

	lastUpdate := time.Now().In(c.location).String()

	_, err := c.client.HGet(context, hashKey, "created").Result()

	if err != nil {
		_, err = c.client.HSet(context, hashKey, "created", lastUpdate).Result()
		if err != nil {
			return fmt.Errorf("engine hash not set: %v", err)
		}
	}
	_, err = c.client.Expire(context, hashKey, c.infoTTL).Result()
	if err != nil {
		return fmt.Errorf("engine hash expiration not set: %v", err)
	}

	return nil
}

func (c *RedisXrayCachingClient) SetXrayInfo(context context.Context, info *contracts.XrayInfo) error {
	hashKey := "engines:" + c.engineID
	running := "true"
	if !info.Running {
		running = "false"
	}

	_, err := c.client.HSet(context, hashKey, "uuid", info.XrayUUID, "running", running).Result()
	if err != nil {
		return fmt.Errorf("xray info not set: %v", err)
	}
	_, err = c.client.Expire(context, hashKey, c.infoTTL).Result()
	if err != nil {
		return fmt.Errorf("engine hash expiration not set: %v", err)
	}

	return nil
}
