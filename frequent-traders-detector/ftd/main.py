#!/usr/bin/env python

import asyncio
import websockets
import json
import time
import requests
from collections import defaultdict
from kafka import KafkaProducer

class TradersDetector:
    def __init__(self, time_limit, tptl):
        self.time_limit = time_limit  # time limit in seconds
        self.tptl = tptl  # Transaction Per Time Limit
        self.possible_traders = defaultdict(lambda: 0)  # dict mapping wallets
        # to time the wallet was involved in a trade
        self.last_trade = {}  # dict mapping each wallet to the last traded time
        self.sent_traders = set()  # wallets that have been already sent to DB
        self.frequent_traders = set()  # mapping wallet of frequent traders to
        # sent or not sent (kafka)

        self.producer = KafkaProducer(
            bootstrap_servers="127.0.0.1:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def getBalance(self, wallet):
        """
        Returns the total btc in the account
        """
        url = "https://blockchain.info/balance?active=" + wallet
        data = requests.get(url).json()
        return data[wallet]["final_balance"]  # unit satoshi

    def kafka_send_frequent_traders(self):
        """
        sends through kafka the frequent traders
        """
        for addr in self.frequent_traders:
            balance = self.getBalance(addr)
            obj = {"addr": addr, "balance": balance}
            self.producer.send("frequent-traders", value=obj)
        self.sent_traders |= self.frequent_traders
        print(f"sent_traders{self.sent_traders}")
        self.frequent_traders.clear()

    def data_structures_processing(self):
        """
        Checks if a frequent trader is detected by iterating through
        possible_traders and last_traders. And if a frequent trader is detected
        add it to member variable frequent_traders
        """
        current_time = time.time()
        addr_to_remove = []
        for addr, last_time in self.last_trade.items():
            if current_time - last_time > self.time_limit:
                addr_to_remove.append(addr)
            elif self.possible_traders[addr] > self.tptl:
                # time_limit not reached and more than
                # transaction_per_time_limit trades
                self.frequent_traders.add(addr)
                addr_to_remove.append(addr)
            # if tl not reached and less than trades than transactions
            # per time limit do nothing
        # remove addreses:
        for addr in addr_to_remove:
            self.last_trade.pop(addr)
            self.possible_traders.pop(addr)
        self.kafka_send_frequent_traders()

    def get_inputs(self, tx):
        inputs = set()
        for input_ in tx["x"]["inputs"]:
            addr = input_["prev_out"]["addr"]
            if addr is None:  # why wtf??
                return inputs
            inputs.add(addr)
        return inputs

    def get_outputs(self, tx):
        outputs = set()
        for out in tx["x"]["out"]:
            out_addr = out["addr"]
            if out_addr is None:  # really wtf?
                return outputs
            outputs.add(out_addr)
        return outputs

    async def main(self):
        async with websockets.connect("wss://ws.blockchain.info/inv") as client:
            print("[main] Connected to wss://ws.blockchain.info/inv")

            cmd = '{"op":"unconfirmed_sub"}'
            await client.send(cmd)

            last_time = time.time()
            while True:
                message = await client.recv()
                dictm = json.loads(message)
                for input_addr in self.get_inputs(dictm):
                    if input_addr in self.sent_traders:
                        continue
                    self.possible_traders[input_addr] += 1
                    self.last_trade[input_addr] = time.time()
                for out_addr in self.get_outputs(dictm):
                    if out_addr in self.sent_traders:
                        continue
                    self.possible_traders[out_addr] += 1
                    self.last_trade[out_addr] = time.time()
                if time.time() - last_time >= time_limit / 2:
                    # if time_limit / 2 seconds passed schedule task to
                    # process data
                    self.data_structures_processing()
                    # asyncio.create_task()
                    last_time = time.time()


if __name__ == "__main__":
    time_limit = 60
    tptl = 3  # transaction per time limit
    app = TradersDetector(time_limit, tptl)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.main())
