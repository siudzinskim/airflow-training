#!/bin/bash

# Script to scale Airflow deployments on microk8s to 0 or 1

# Check if the replica count is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <replicas>"
  echo "  <replicas>: 0 or 1"
  exit 1
fi

REPLICAS=$1

# Validate the replica count
if [ "$REPLICAS" -ne 0 ] && [ "$REPLICAS" -ne 1 ]; then
  echo "Error: Invalid replica count. Please use 0 or 1."
  echo "Usage: $0 <replicas>"
  exit 1
fi

# List of deployments to scale
DEPLOYMENTS=(
  "airflow-api-server"
  "airflow-dag-processor"
  "airflow-scheduler"
  "airflow-statsd"
)

NAMESPACE="airflow"

echo "Scaling Airflow deployments to $REPLICAS replicas in namespace '$NAMESPACE'..."

for DEPLOYMENT in "${DEPLOYMENTS[@]}"; do
  echo "Scaling deployment/$DEPLOYMENT..."
  microk8s kubectl scale --replicas=$REPLICAS deployment/$DEPLOYMENT -n $NAMESPACE
done

echo "Scaling complete."
