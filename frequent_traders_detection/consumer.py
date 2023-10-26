from kafka import KafkaConsumer

consumer = KafkaConsumer('frequent-traders')
for msg in consumer:
    print(msg)
