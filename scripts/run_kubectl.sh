#!/bin/bash


wait_for_running_resource(){


}
current_path=$(pwd)

echo "Running k8s infrastructure locally"
minikube start --memory=8192 --cpus=3 -p trade-mirror
# Operator
kubectl apply -f 'https://strimzi.io/install/latest?namespace=default' -n default
#wait_for_running_resource 

# configmaps
kubectl apply -f "$current_path/infrastructure/kubernetes/configmaps" -n default

# my-cluster
kubectl apply -f "$current_path/infrastructure/kubernetes/kafka/" -n default
# wait_for_running_resource

# frequent-traders topic
kubectl apply -f "$current_path/infrastructure/kubernetes/kafka_topics/" -n default
# wait_for_running_resource

# kubectl apply -f "$current_path/infrastructure/kubernetes/kafka" -n default

kubectl apply -f "$current_path/infrastructure/kubernetes/deployments" -n default

kubectl apply -f "$current_path/infrastructure/kubernetes/services" -n default

kubectl get pods -n default
