import redis
import json
import requests
import os
from kafka import KafkaConsumer


def getBalance(wallet):
    """
    Returns the total btc in the account
    """
    url = "https://blockchain.info/balance?active=" + wallet
    data = requests.get(url).json()
    return data[wallet]["final_balance"]  # unit satoshi


def main():
    redis_host = os.environ.get("REDIS_HOST")
    redis_port = os.environ.get("REDIS_PORT")
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
    bootstrap_server = os.environ.get("BOOTSTRAP_SERVER")
    frequent_traders_topic = os.environ.get("TOPIC_FREQUENT_TRADERS")
    consumer = KafkaConsumer(
        frequent_traders_topic,
        bootstrap_servers=bootstrap_server,
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
