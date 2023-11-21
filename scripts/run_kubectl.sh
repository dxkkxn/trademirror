#!/bin/bash

# minikube stop

current_path=$(pwd)
echo "Running k8s infrastructure locally"
minikube start --memory=8192 --cpus=3 -p kafka

echo "Finally configure to use minikube internal docker as docker host:"

eval $(minikube docker-env -p kafka)

kubectl apply -f 'https://strimzi.io/install/latest?namespace=default' -n default

kubectl apply -f "$current_path/infrastructure/kubernetes/configmaps" -n default

# kubectl apply -f "$current_path/infrastructure/kubernetes/kafka" -n default

kubectl apply -f "$current_path/infrastructure/kubernetes/deployments" -n default

kubectl apply -f "$current_path/infrastructure/kubernetes/services" -n default

kubectl get pods -n default
