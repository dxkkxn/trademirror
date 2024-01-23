#!/usr/bin/python3

from redis import StrictRedis
import redis
import requests
import websockets
import asyncio
import json
import os
from enum import Enum
from queue import Queue

import time
import threading
from kafka import KafkaConsumer

OP = Enum("OP", ["BUY", "SELL"])


def get_inputs(tx):
    inputs = set()
    for input_ in tx["x"]["inputs"]:
        inputs.add(input_["prev_out"]["addr"])
    return inputs


def get_outputs(tx):
    outputs = set()
    for out in tx["x"]["out"]:
        out_addr = out["addr"]
        outputs.add(out_addr)
    return outputs


def get_tx_input(tx_l, wallet):
    for tx in tx_l:
        if wallet == tx["prev_out"]["addr"]:
            return tx["prev_out"]
    raise NotImplementedError("wtf?")


def get_tx_output(tx_l, wallet):
    for tx in tx_l:
        if wallet == tx["addr"]:
            return tx
    raise NotImplementedError("wtf?")


def get_bitcoin_price():
    res = requests.get("https://api.blockchain.com/v3/exchange/tickers/BTC-USD").json()
    return res["last_trade_price"]


async def compute_tx(op, wallet, tx, transaction_queue: Queue):
    current_balance = int(REDIS_CLIENT.hget(wallet, "balance").decode("utf-8"))
    btc_price = get_bitcoin_price()  # in usd
    if op == OP.SELL:
        tx = get_tx_input(tx["x"]["inputs"], wallet)
        new_op = {
            "op": "SELL",
            "btc_price": btc_price,
            "current_balance": current_balance,
            "value": tx["value"],
        }
        await transaction_queue.put(new_op)
        REDIS_CLIENT.lpush(wallet + ":op", json.dumps(new_op))
        REDIS_CLIENT.hset(wallet, "balance", current_balance - tx["value"])
    else:
        assert op == OP.BUY
        tx = get_tx_output(tx["x"]["out"], wallet)
        new_op = {
            "op": "BUY",
            "btc_price": btc_price,
            "current_balance": current_balance,
            "value": tx["value"],
        }
        await transaction_queue.put(new_op)
        REDIS_CLIENT.lpush(wallet + ":op", json.dumps(new_op))
        REDIS_CLIENT.hset(wallet, "balance", current_balance + tx["value"])
    print(f"updated wallet {wallet}")
    # print(redis_client.hgetall(wallet))
    # print(redis_client.lrange(wallet+":op", 0, -1))


WALLETS = None
REDIS_CLIENT = None
USER_BALANCE = {"btc": 0, "fiat": 0}
USER_WALLETS = {}


def main(transaction_queue: Queue):
    
    new_user_wallets = {}
    for item in REDIS_CLIENT.smembers("users:tracking:default_user"):
        wallet_hash = str(item)
        if wallet_hash not in new_user_wallets:
            new_user_wallets.add(wallet_hash)
    USER_WALLETS = new_user_wallets

    bootstrap_server = os.environ.get("BOOTSTRAP_SERVER")
    interesting_transactions = os.environ.get("TOPIC_INTERESTING_TRANSACTIONS")
    consumer = KafkaConsumer(
        interesting_transactions,
        bootstrap_servers=bootstrap_server,
        group_id="balance-fetcher",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
    print("Initialized succesfully")
    for msg in consumer:
        op = json.loads(msg)
        transaction_queue.put(op)


def handle_wallet_tracking_event(msg):
    global REDIS_CLIENT
    new_user_wallets = {}
    for item in REDIS_CLIENT.smembers("users:tracking:default_user"):
        wallet_hash = str(item)
        if wallet_hash not in new_user_wallets:
            new_user_wallets.add(wallet_hash)
    USER_WALLETS = new_user_wallets


def worker(queue: asyncio.Queue):
    global REDIS_CLIENT

    print("Started transaction replicaiton worker...")
    while not REDIS_CLIENT.exists("users:balance"):
        time.sleep(2)
        print("Waiting for user balance to be synchronized...")

    user_balance = json.loads(str(REDIS_CLIENT.hget("users:balance", "default_user")))
    USER_BALANCE["fiat"] = user_balance["fiat"]
    USER_BALANCE["btc"] = user_balance["btc"]

    should_run = True
    while should_run:
        print("replication thread loop working...")
        while not transaction_queue.empty():
            transaction = queue.get()

            if transaction is None:
                should_run = False
                break
            
            print("Processing transaction...")
            if transaction["op"] == "BUY":
                USER_BALANCE["fiat"] -= (transaction["value"] / 100000000) * transaction[
                    "btc_price"
                ]
                USER_BALANCE["btc"] += transaction["value"]
            elif transaction["op"] == "SELL":
                USER_BALANCE["fiat"] += (transaction["value"] / 100000000) * transaction[
                    "btc_price"
                ]
                USER_BALANCE["btc"] -= transaction["value"]

            transaction["current_balance"] = USER_BALANCE["fiat"]
            REDIS_CLIENT.rpush("users:transactions:default_user", json.dumps(transaction))
            REDIS_CLIENT.hset("users:balance", "default_user", json.dumps(USER_BALANCE))
        time.sleep(1)

if __name__ == "__main__":
    redis_host = os.environ.get("REDIS_HOST")
    redis_port = os.environ.get("REDIS_PORT")
    REDIS_CLIENT = StrictRedis(host=redis_host, port=redis_port, db=0)

    pubsub = REDIS_CLIENT.pubsub()

    # subscribe to events on the wallets being followed
    pubsub.psubscribe(
        **{"__keyspace@0__:users:tracking:default_user": handle_wallet_tracking_event}
    )

    pubsub.run_in_thread(sleep_time=0.01)

    # transaction_queue = asyncio.Queue()
    # worker_thread = threading.Thread(target=worker, args=(transaction_queue))
    # worker_thread.start()

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main(transaction_queue))
    
    # worker_thread.join()

    new_loop = asyncio.get_event_loop()
    transaction_queue = asyncio.Queue()

    producer_thread = threading.Thread(target=lambda: new_loop.run_until_complete(main(transaction_queue)))
    consumer_thread = threading.Thread(target=lambda: new_loop.run_until_complete(worker(transaction_queue)))

    producer_thread.start()
    consumer_thread.start()
    producer_thread.join()

    new_loop.run_until_complete(transaction_queue.put(None))
    consumer_thread.join()

    # new_loop.close()