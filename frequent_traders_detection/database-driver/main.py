import redis
from kafka import KafkaConsumer

redis_client = redis.Redis(host="localhost", port=6379, db=0)
consumer = KafkaConsumer('frequent-traders')

for msg in consumer:
    print(f"msg received {msg.value}")
    redis_client.lpush("frequent-trading-wallets", msg.value)
