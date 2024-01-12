#!/usr/bin/python3

from redis import StrictRedis
from threading import Thread
import requests
import websockets
import asyncio
import json
import os
from kafka import KafkaConsumer
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
    res = requests.get("https://api.blockchain.com/v3/exchange/tickers/BTC-USD").json()
    return res["last_trade_price"]


bootstrap_server = os.environ.get("BOOTSTRAP_SERVER")
frequent_traders_topic = os.environ.get("TOPIC_TRANSACTIONS")
# producer = KafkaProducer(
#     bootstrap_servers=bootstrap_server,
#     value_serializer=lambda v: json.dumps(v).encode("utf-8"),
# )

def compute_tx(op, wallet, tx):
    balance = REDIS_CLIENT.hget(wallet, 'balance')
    while not balance: # this can happen bc tf is faster than insertion
        balance = REDIS_CLIENT.hget(wallet, 'balance')
    current_balance = int(balance.decode('utf-8'))
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

    REDIS_CLIENT.lpush(wallet+":op", json.dumps(new_op))
    REDIS_CLIENT.hset(wallet, "balance", value)
    print(f"updated wallet {wallet}")
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



def get_new_wallets():
    bootstrap_server = os.environ.get("BOOTSTRAP_SERVER")
    frequent_traders_topic = os.environ.get("TOPIC_FREQUENT_TRADERS")
    consumer = KafkaConsumer(
        frequent_traders_topic,
        bootstrap_servers=bootstrap_server,
        group_id="transaction-fetcher",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
    for msg in consumer:
        print(f"new wallet received {msg.value}")
        WALLETS.append(msg.value)



if __name__ == "__main__":
    redis_host = os.environ.get("REDIS_HOST")
    redis_port = os.environ.get("REDIS_PORT")
    REDIS_CLIENT = StrictRedis(host=redis_host, port=redis_port, db=0)
    # WALLETS = REDIS_CLIENT.lrange("frequent-trading-wallets", 0, -1)
    # WALLETS = set(w.decode('utf-8') for w in WALLETS)
    # pubsub = REDIS_CLIENT.pubsub()
    # pubsub.psubscribe(**{"__keyspace@0__:frequent-trading-wallets": event_handler})
    # pubsub.run_in_thread(sleep_time=0.01)
    t1 = Thread(target=get_new_wallets)
    t1.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
