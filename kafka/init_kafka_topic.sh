#!/bin/bash

KAFKA_TOPICS_SCRIPT="$KAFKA_HOME/bin/kafka-topics.sh"
# KAFKA_SERVER="kafka:9092"  # Use the service name defined in your docker-compose file
# KAFKA_SERVER="localhost:9092"  # Use the service name defined in your docker-compose file
TOPIC_NAME="frequent-traders"

echo "Waiting for Kafka to be reachable at $KAFKA_SERVER..."

# Check if Kafka is reachable
while ! nc -z kafka 9092; do
  sleep 1
done

echo "Kafka is reachable. Creating topic '$TOPIC_NAME'..."

# Create Kafka topic
"$KAFKA_TOPICS_SCRIPT" --create --topic "$TOPIC_NAME" --bootstrap-server "$KAFKA_SERVER" --replication-factor 1 --partitions 1

