package caching

import (
	"time"

	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
)

func CreateRedisXrayCachingClient(addr string, password string, infoTTL time.Duration, timezone string) (*RedisXrayCachingClient, error) {
	client := redis.NewClient(&redis.Options{Addr: addr, Password: password})
	loc, err := time.LoadLocation(timezone)
	if err != nil {
		return nil, err
	}
	return &RedisXrayCachingClient{client: client, engineID: uuid.New().String(), infoTTL: infoTTL, location: loc}, nil
}
