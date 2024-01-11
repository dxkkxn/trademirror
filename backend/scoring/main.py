#!/usr/bin/python3

from redis import StrictRedis
import json


def compute_score(wallets, redis_client):
    for wallet in wallets:
        wop = (redis_client.lrange(f"{wallet}:op", 0, -1))
        ops = [json.loads(op) for op in wop]
        if len(ops) <= 1:
            redis_client.hset(wallet, 'score', 0)
            continue
        # print()
        # print()
        # 1 BTC = 10_0000_000 Satoshi
        # wallet_value = 0
        score = 0
        last_buy_price = None
        for op in reversed(ops):
            if op['op'] == 'BUY':
                last_buy_price = op['btc_price'];
                # wallet_value += op['value'] * (op['btc_price'] * (10**-8))
            if op['op'] == 'SELL':
                # wallet_value -= op['value'] * (op['btc_price'] * (10**-8))
                sell_price = op['btc_price'];
                if last_buy_price == None:
                    continue;
                if last_buy_price < sell_price:
                    score += 1
        redis_client.hset(wallet, "score", score)
    # print("finished")


            # print(op)

        # print(ops)
        # json.loads(wop)
    # print(wallets)


if __name__ == "__main__":
    redis_client = StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
    wallets = redis_client.lrange("frequent-trading-wallets", 0, -1)
    compute_score(wallets, redis_client)

    # pubsub = REDIS_CLIENT.pubsub()
    # pubsub.psubscribe(**{"__keyspace@0__:frequent-trading-wallets": event_handler})
    # pubsub.run_in_thread(sleep_time=0.01)
