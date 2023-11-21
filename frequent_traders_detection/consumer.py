import redis
from confluent_kafka import Consumer, KafkaException
import sys
import os

# from kafka import KafkaConsumer

redis_client = redis.Redis(host="redis", port=6379, db=0)
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
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        print("Received message: {0}".format(msg.value()))
        # print("Received message: {0}".format(msg))
        redis_client.lpush("frequent-trading-wallets", msg.value())
except KeyboardInterrupt:
    sys.stderr.write("aborted by user.")
finally:
    consumer.close()


# for msg in consumer:
#     print(f"msg received {msg.value}")
