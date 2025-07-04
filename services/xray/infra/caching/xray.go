package caching

import (
	"context"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/infanasotku/netku/services/xray/contracts"
	"github.com/redis/go-redis/v9"
)

type RedisXrayCachingClient struct {
	client   *redis.Client
	infoTTL  time.Duration
	engineID string
	location *time.Location
}

func getHashKey(uuid string) string {
	return "xrayEngines:" + uuid
}

func (c *RedisXrayCachingClient) CreateWithTTL(context context.Context, extraFields ...interface{}) error {
	hashKey := getHashKey(c.engineID)
	created := time.Now().In(c.location).Format(time.RFC3339Nano)

	fields := append(extraFields, "created", created, "event_id", uuid.New().String())
	_, err := c.client.HSet(context, hashKey, fields...).Result()
	if err != nil {
		return fmt.Errorf("xray info not created: %v", err)
	}
	_, err = c.client.Expire(context, hashKey, c.infoTTL).Result()
	if err != nil {
		return fmt.Errorf("engine hash expiration not set: %v", err)
	}

	return err
}

func (c *RedisXrayCachingClient) RefreshTTL(context context.Context) error {
	hashKey := getHashKey(c.engineID)

	keys, err := c.client.Exists(context, hashKey).Result()

	if err != nil || keys == 0 {
		return contracts.ErrEngineHashNotFound
	}
	_, err = c.client.Expire(context, hashKey, c.infoTTL).Result()
	if err != nil {
		return fmt.Errorf("engine hash expiration not set: %v", err)
	}

	return nil
}

func (c *RedisXrayCachingClient) SetXrayInfo(context context.Context, info *contracts.XrayInfo) error {
	hashKey := getHashKey(c.engineID)
	running := "true"
	if !info.Running {
		running = "false"
	}

	_, err := c.client.HSet(
		context, hashKey,
		"uuid", info.XrayUUID,
		"running", running,
		"event_id", uuid.New().String(),
	).Result()
	if err != nil {
		return fmt.Errorf("xray info not set: %v", err)
	}
	_, err = c.client.Expire(context, hashKey, c.infoTTL).Result()
	if err != nil {
		return fmt.Errorf("engine hash expiration not set: %v", err)
	}

	return nil
}
