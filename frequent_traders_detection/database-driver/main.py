import redis
import json
from kafka import KafkaConsumer
import os

# -------------- youssef ----------

# redis_client = redis.Redis(host="localhost", port=6379, db=0)
# consumer = KafkaConsumer('frequent-traders',
#                          value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# ------------------------------

# ----------- k8s ---------------
redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")
boostrap_server = os.environ.get("BOOSTRAP_SERVER")
topic_frequent_traders = os.environ.get("TOPIC_FREQUENT_TRADERS")
# print(f"{redis_host} - {redis_port} - {boostrap_server} - {topic_frequent_traders}")

redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
print(boostrap_server)
consumer = KafkaConsumer(
    topic_frequent_traders,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    bootstrap_servers=boostrap_server,  # Assuming 'bootstrap_server' contains server addresses
)
# --------------------------------

for msg in consumer:
    print(f"msg received {msg.value}")
    addr = msg.value["addr"]
    balance = msg.value["balance"]
    redis_client.lpush("frequent-trading-wallets", addr)
    redis_client.hset(addr, "balance", balance)
