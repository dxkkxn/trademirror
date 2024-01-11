#!/usr/bin/python3

from redis import StrictRedis
import json

# def compute_score(wallets, redis_client):

REDIS_CLIENT = StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

def compute_score(wallet):
    print(f"computing score for wallet {wallet}...")
    wop = (REDIS_CLIENT.lrange(f"{wallet}:op", 0, -1))
    ops = [json.loads(op) for op in wop]
    if len(ops) <= 1:
        REDIS_CLIENT.hset(wallet, 'score', 0)
    # print()
    # print()
    # 1 BTC = 10_0000_000 Satoshi
    # wallet_value = 0
    score = 0
    last_buy_price = None
    for op in reversed(ops):
        if op['op'] == 'BUY':
            last_buy_price = op['btc_price']
            # wallet_value += op['value'] * (op['btc_price'] * (10**-8))
        if op['op'] == 'SELL':
            # wallet_value -= op['value'] * (op['btc_price'] * (10**-8))
            sell_price = op['btc_price']
            if last_buy_price == None:
                continue;
            if last_buy_price < sell_price:
                score += 1
    REDIS_CLIENT.hset(wallet, "score", score)


def event_handler(msg):
    print(msg)
    wallet = msg['channel'].split(':')[-2]
    compute_score(wallet)


if __name__ == "__main__":
    wallets = REDIS_CLIENT.lrange("frequent-trading-wallets", 0, -1)
    for wallet in wallets:
        compute_score(wallet)

    pubsub = REDIS_CLIENT.pubsub()
    pubsub.psubscribe(**{"__keyspace@0__:*:op": event_handler})
    pubsub.run_in_thread(sleep_time=0.01)
