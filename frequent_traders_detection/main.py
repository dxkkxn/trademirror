#!/usr/bin/env python

import asyncio
import websockets
import json
import time
from collections import defaultdict
from kafka import KafkaProducer


class TradersDetector:

    def __init__(self, time_limit, tptl):
        self.time_limit = time_limit  # time limit in seconds
        self.tptl = tptl  # Trasaction Per Time Limit
        self.possible_traders = defaultdict(lambda: 0)  # dict mapping wallets
        # to time the wallet was involved in a trade
        self.last_trade = {}  # dict mapping each wallet to the last traded time
        self.frequent_traders = set()

        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')

    async def data_structures_processing(self):
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
            # if tl not reached and less than trades than transactions
            # per time limit do nothing
        # remove addreses:
        for addr in addr_to_remove:
            self.last_trade.pop(addr)
            self.possible_traders.pop(addr)

        print(
            f"size of frequent traders= {len(self.frequent_traders)}, ft ={self.frequent_traders}"
        )

        for addr in self.frequent_traders:
            self.producer.send('frequent-traders',
                               bytes(addr, encoding='utf-8'))
        return

    async def main(self):
        async with websockets.connect("wss://ws.blockchain.info/inv") as client:
            print("[main] Connected to wss://ws.blockchain.info/inv")

            cmd = '{"op":"unconfirmed_sub"}'
            await client.send(cmd)

            last_time = time.time()
            while True:
                message = await client.recv()
                dictm = json.loads(message)
                for input_ in dictm["x"]["inputs"]:
                    input_addr = input_["prev_out"]["addr"]
                    self.possible_traders[input_addr] += 1
                    self.last_trade[input_addr] = time.time()
                for out in dictm["x"]["out"]:
                    out_addr = out["addr"]
                    self.possible_traders[out["addr"]] += 1
                    self.last_trade[out_addr] = time.time()
                # if time.time() - last_time >= time_limit/2:
                    # if time_limit / 2 seconds passed schedule task to
                    # process data
                asyncio.create_task(self.data_structures_processing())
                last_time = time.time()



if __name__ == "__main__":
    time_limit = 60
    tptl = 3  # transaction per time limit
    app = TradersDetector(time_limit, tptl)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.main())
