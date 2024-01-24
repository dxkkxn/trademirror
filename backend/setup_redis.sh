#!/usr/bin/bash

redis-server /redis.conf &
sleep 5
redis-cli sadd "wallets:replication:wallet" "default_user"
redis-cli hset "users:balance" "default_user" '{"fiat": 100000, "btc": 1}'
tail -f /dev/null
