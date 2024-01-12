#!/bin/bash

topic="frequent-traders"

# Check if the topic exists
existing_topics=$(kafka-topics --list --bootstrap-server kafka:29092)

if [[ $existing_topics == *"$topic"* ]]; then
  echo "Topic '$topic' already exists."
else
  # Create the topic if it doesn't exist
  kafka-topics --create --bootstrap-server kafka:29092 --replication-factor 1 --partitions 6 --topic "$topic"
  kafka-topics --create --bootstrap-server kafka:29092 --replication-factor 1 --partitions 6 --topic "transactions"
  echo "Topic '$topic' has been created."
fi

