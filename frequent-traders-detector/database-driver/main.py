import redis
import json
from kafka import KafkaConsumer

redis_client = redis.Redis(host="localhost", port=6379, db=0)
consumer = KafkaConsumer('frequent-traders',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for msg in consumer:
    print(f"msg received {msg.value}")
    addr = msg.value['addr']
    balance = msg.value['balance']
    redis_client.lpush("frequent-trading-wallets", addr)
    redis_client.hset(addr, 'balance', balance)