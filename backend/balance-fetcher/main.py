import redis
import json
import requests
from kafka import KafkaConsumer


def getBalance(wallet):
    """
    Returns the total btc in the account
    """
    url = "https://blockchain.info/balance?active=" + wallet
    data = requests.get(url).json()
    return data[wallet]["final_balance"]  # unit satoshi


def main():
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    consumer = KafkaConsumer(
        "frequent-traders",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
    print("Initialized succesfully")
    for msg in consumer:
        print(f"msg received {msg.value}")
        addr = msg.value
        balance = getBalance(addr)
        redis_client.lpush("frequent-trading-wallets", addr)
        redis_client.hset(addr, 'balance', balance)


if __name__ == "__main__":
    main()
