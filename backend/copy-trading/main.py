#!/usr/bin/python3

from redis import StrictRedis
import json
import os
from kafka import KafkaConsumer

WALLETS = None
REDIS_CLIENT = None
USER_BALANCE = {"btc": 0, "fiat": 0}
USER_WALLETS = set()

def handle_wallet_tracking_event(msg):
    global REDIS_CLIENT, USER_WALLETS
    print("new wallet to track received...")
    USER_WALLETS = REDIS_CLIENT.smembers("users:tracking:default_user")
    print(f"tracking wallets {USER_WALLETS}")

def to_btc(satoshi):
    return satoshi / 100_000_000


def main():
    global USER_WALLETS
    for wallet in REDIS_CLIENT.smembers("users:tracking:default_user"):
        print(wallet)
        if wallet not in USER_WALLETS:
            USER_WALLETS.add(wallet)

    bootstrap_server = os.environ.get("BOOTSTRAP_SERVER")
    interesting_transactions = os.environ.get("TOPIC_TRANSACTIONS")
    consumer = KafkaConsumer(
        interesting_transactions,
        bootstrap_servers=bootstrap_server,
        group_id="balance-fetcher",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    REDIS_CLIENT.hset("users:balance", "default_user", '{"fiat": 100, "btc": 1}')
    user_balance = json.loads(REDIS_CLIENT.hget("users:balance", "default_user"))
    print(user_balance, type(user_balance))
    USER_BALANCE["fiat"] = user_balance["fiat"]
    USER_BALANCE["btc"] = user_balance["btc"]
    print("Initialized succesfully")
    for msg in consumer:
        transaction = msg.value
        print(f"tx received {transaction}")
        if transaction['wallet'] not in USER_WALLETS:
            continue
        print(f"tx received {transaction}")
        print("Processing transaction...")
        if transaction["current_balance"] == 0 or \
           transaction["value"] == transaction["current_balance"]:
            continue
        percentage = transaction["value"] / transaction["current_balance"]


        if transaction["op"] == "BUY":
            value_to_buy = USER_BALANCE["fiat"] * percentage
            USER_BALANCE["fiat"] -= value_to_buy
            USER_BALANCE["btc"] += value_to_buy / transaction["btc_price"]
        elif transaction["op"] == "SELL":
            value_to_sell = USER_BALANCE['btc'] * percentage
            USER_BALANCE["btc"] -= value_to_sell
            USER_BALANCE["fiat"] += to_btc(value_to_sell) * transaction["btc_price"]
        print(USER_BALANCE)
        transaction["current_balance"] = USER_BALANCE["fiat"]
        REDIS_CLIENT.rpush("users:transactions:default_user", json.dumps(transaction))
        REDIS_CLIENT.hset("users:balance", "default_user", json.dumps(USER_BALANCE))

if __name__ == "__main__":
    redis_host = os.environ.get("REDIS_HOST")
    redis_port = os.environ.get("REDIS_PORT")
    REDIS_CLIENT = StrictRedis(host=redis_host, port=redis_port,
                               decode_responses=True, db=0)
    pubsub = REDIS_CLIENT.pubsub()

    # subscribe to events on the wallets being followed
    pubsub.psubscribe(
        **{"__keyspace@0__:users:tracking:default_user": handle_wallet_tracking_event}
    )

    print("Starting...")
    pubsub.run_in_thread(sleep_time=0.01)
    print("finished")
    main()
