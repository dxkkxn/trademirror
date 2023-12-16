#!/bin/bash

topic="frequent-traders"

# Run kafka-topics command and capture the output
topics_list=$(kafka-topics --list --bootstrap-server kafka:29092)

# Check if the topic exists in the output
if [[ $topics_list == *"$topic"* ]]; then
  echo "topic exists"
  exit 0  # Topic exists, return success (exit code 0)
else
  exit 1  # Topic does not exist, return failure (exit code 1)
fi

