#!/usr/bin/python3

from redis import StrictRedis
from threading import Thread
import requests
import websockets
import asyncio
import json
import os
from kafka import KafkaConsumer, KafkaProducer
from enum import Enum

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
    res = requests.get("https://blockchain.info/ticker").json()
    return res['USD']['last']


bootstrap_server = os.environ.get("BOOTSTRAP_SERVER")
topic_transactions = os.environ.get("TOPIC_TRANSACTIONS")
producer = KafkaProducer(
    bootstrap_servers=bootstrap_server,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def compute_tx(op, wallet, tx):
    current_balance = int(REDIS_CLIENT.hget(wallet, 'balance'))
    btc_price = get_bitcoin_price() # in usd
    value = 0

    if op == OP.SELL:
        tx = get_tx_input(tx["x"]["inputs"], wallet)
        new_op = {
            "op": "SELL",
            "btc_price": btc_price,
            "current_balance": current_balance,
            "value": tx["value"],
        }
        value = current_balance-tx['value'];
    else:
        assert op == OP.BUY
        tx = get_tx_output(tx["x"]["out"], wallet)
        new_op = {
            "op": "BUY",
            "btc_price": btc_price,
            "current_balance": current_balance,
            "value": tx["value"],
        }
        value = current_balance+tx['value'];

    if tx["value"] <= 0 or current_balance <= 0 or value <= 0:
        return;

    REDIS_CLIENT.lpush(wallet+":op", json.dumps(new_op))
    REDIS_CLIENT.hset(wallet, "balance", value)
    print(f"updated wallet {wallet}")
    new_op["wallet"] = wallet
    producer.send(topic_transactions, value=new_op)
    print(f"new transaction sent to {topic_transactions}")
    # print(redis_client.hgetall(wallet))
    # print(redis_client.lrange(wallet+":op", 0, -1))



WALLETS = []
REDIS_CLIENT = None
async def main():
    async with websockets.connect("wss://ws.blockchain.info/inv") as client:
        print("[main] Connected to wss://ws.blockchain.info/inv")
        cmd = '{"op":"unconfirmed_sub"}'
        await client.send(cmd)
        message = await client.recv()
        dictm = json.loads(message)

        while True:
            message = await client.recv()
            dictm = json.loads(message)
            for input_addr in get_inputs(dictm):
                if input_addr in WALLETS:
                    compute_tx(OP.SELL, input_addr, dictm)
            for out_addr in get_outputs(dictm):
                if out_addr in WALLETS:
                    compute_tx(OP.BUY, out_addr, dictm)



def event_handler(msg):
    global WALLETS
    wallets = REDIS_CLIENT.lrange("frequent-trading-wallets", 0, -1)
    WALLETS = set(wallets)
    print(f"tracking {len(WALLETS)} wallets")


if __name__ == "__main__":
    redis_host = os.environ.get("REDIS_HOST")
    redis_port = os.environ.get("REDIS_PORT")
    REDIS_CLIENT = StrictRedis(host=redis_host, port=redis_port, db=0,
                               decode_responses=True)
    WALLETS = set(REDIS_CLIENT.lrange("frequent-trading-wallets", 0, -1))
    pubsub = REDIS_CLIENT.pubsub()
    pubsub.psubscribe(**{"__keyspace@0__:frequent-trading-wallets": event_handler})
    pubsub.run_in_thread(sleep_time=0.01)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
