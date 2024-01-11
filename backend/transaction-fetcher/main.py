#!/usr/bin/python3

from redis import StrictRedis
import requests
import websockets
import asyncio
import json
from enum import Enum
OP = Enum("OP", ['BUY', 'SELL'])

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
        if wallet == tx['prev_out']['addr']:
            return tx['prev_out']
    raise NotImplementedError('wtf?')

def get_tx_output(tx_l, wallet):
    for tx in tx_l:
        if wallet == tx['addr']:
            return tx
    raise NotImplementedError('wtf?')

def get_bitcoin_price():
    res = requests.get("https://api.blockchain.com/v3/exchange/tickers/BTC-USD").json()
    return res['last_trade_price']

def compute_tx(op, wallet, tx):
    current_balance = int(REDIS_CLIENT.hget(wallet, 'balance').decode('utf-8'))
    btc_price = get_bitcoin_price() # in usd
    if op == OP.SELL:
        tx = get_tx_input(tx['x']['inputs'], wallet)
        new_op = {
            'op': 'SELL',
            'btc_price': btc_price,
            'current_balance': current_balance,
            'value': tx['value']
        }
        REDIS_CLIENT.lpush(wallet+":op", json.dumps(new_op))
        REDIS_CLIENT.hset(wallet, "balance", current_balance-tx['value'])
    else:
        assert(op == OP.BUY)
        tx = get_tx_output(tx['x']['out'], wallet)
        new_op = {
            'op': 'BUY',
            'btc_price': btc_price,
            'current_balance': current_balance,
            'value': tx['value']
        }
        REDIS_CLIENT.lpush(wallet+":op", json.dumps(new_op))
        REDIS_CLIENT.hset(wallet, "balance", current_balance+tx['value'])
    print(f"updated wallet {wallet}")
    # print(redis_client.hgetall(wallet))
    # print(redis_client.lrange(wallet+":op", 0, -1))



WALLETS = None
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
    WALLETS = REDIS_CLIENT.lrange("frequent-trading-wallets", 0, -1)
    WALLETS = set(w.decode('utf-8') for w in WALLETS)
    print("tracking {len(WALLETS)} wallets")



if __name__ == "__main__":
    REDIS_CLIENT = StrictRedis(host="localhost", port=6379, db=0)
    WALLETS = REDIS_CLIENT.lrange("frequent-trading-wallets", 0, -1)
    WALLETS = set(w.decode('utf-8') for w in WALLETS)
    pubsub = REDIS_CLIENT.pubsub()
    pubsub.psubscribe(**{"__keyspace@0__:frequent-trading-wallets": event_handler})
    pubsub.run_in_thread(sleep_time=0.01)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
