#!/usr/bin/env python

import asyncio
import websockets
import json
import time
from collections import defaultdict

time_limit = 10 * 60; # 10 min
trades_per_tl = 3; # trades per time limit

async def main():
    async with websockets.connect("wss://ws.blockchain.info/inv") as client:
        print("[main] Connected to wss://ws.blockchain.info/inv" )

        cmd = '{"op":"unconfirmed_sub"}'
        await client.send(cmd)

        possible_traders = defaultdict(lambda: 0)  # dict mapping wallets to time the
                                           # wallet was involved in a trade
        last_trade = {}  # dict mapping each wallet to the last traded time
        frequent_traders = set()
        while True:
            message = await client.recv()
            dictm = json.loads(message)
            # print('[main] Recv:', message)
            print('input')
            for input_ in dictm['x']['inputs']:
                print(input_)
                input_addr = input_['prev_out']['addr']
                print(input_addr)
                possible_traders[input_addr] += 1
                last_trade[input_addr] = time.time()
            print('out')
            for out in dictm['x']['out']:
                out_addr = out['addr']
                print(out_addr)
                possible_traders[out['addr']] += 1
                last_trade[out_addr] = time.time()

            current_time = time.time()
            addr_to_remove = []
            for addr, last_time in last_trade.items():
                if current_time - last_time > time_limit:
                    addr_to_remove.append(addr)
                elif possible_traders[addr] > trades_per_tl:
                    # time_limit not reached and more than trades_per_tl trades
                    frequent_traders.add(addr)
                # if tl not reached and less than trades than trades_per_tl do nothing
            # remove addreses:
            for addr in addr_to_remove:
                last_trade.pop(addr)
                possible_traders.pop(addr)

            print(f'size of frequent traders= {len(frequent_traders)}, ft ={frequent_traders}')




if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
