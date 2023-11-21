import redis
from confluent_kafka import Consumer, KafkaException
import sys
import os

# from kafka import KafkaConsumer

# redis_client = redis.Redis(host="redis", port=6379, db=0)
redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
# redis_client = redis.Redis(host="redis", port=6379, db=0)

# consumer = KafkaConsumer('frequent-traders')
consumer_conf = {
    "bootstrap.servers": os.environ.get("BOOSTRAP_SERVER"),
    "client.id": "my-consumer",
    "group.id": "trading-group",
}
topic = "frequent-traders"
consumer = Consumer(consumer_conf)
try:
    consumer.subscribe([topic])
    while True:
        print(consumer)
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"error: {msg.error()}")
            # break
        print("Received message: {0}".format(msg.value()))
        redis_client.lpush("frequent-trading-wallets", msg.value())
except KeyboardInterrupt:
    sys.stderr.write("aborted by user.")
finally:
    consumer.close()


# for msg in consumer:
#     print(f"msg received {msg.value}")
