#!/usr/bin/env sh

set -xe
kafka=kafka_2.13-3.6.0
$kafka/bin/zookeeper-server-start.sh $kafka/config/zookeeper.properties&
sleep 10 #  wait zookeeper launch before launching kafka
$kafka/bin/kafka-server-start.sh $kafka/config/server.properties&
sleep 10 #  wait kafka launch before creating topics
$kafka/bin/kafka-topics.sh --create --topic frequent-traders --bootstrap-server localhost:9092&
