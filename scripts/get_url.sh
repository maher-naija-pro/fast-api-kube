#!/bin/bash

# Set namespace and service variables
NAMESPACE="fast-api-app "
SERVICE="fast-api-kube"

# Fetch the NodePort and handle any potential errors
NODE_PORT=$(kubectl get --namespace $NAMESPACE -o jsonpath="{.spec.ports[0].nodePort}" services $SERVICE 2>/dev/null)
if [ -z "$NODE_PORT" ]; then
  echo "Error: Unable to fetch the NodePort for service '$SERVICE' in namespace '$NAMESPACE'."
  exit 1
fi

# Fetch the Node IP and handle any potential errors
NODE_IP=$(kubectl get nodes --namespace $NAMESPACE -o jsonpath="{.items[0].status.addresses[0].address}" 2>/dev/null)
if [ -z "$NODE_IP" ]; then
  echo "Error: Unable to fetch the Node IP in namespace '$NAMESPACE'."
  exit 1
fi

# Display the URL
URL="http://$NODE_IP:$NODE_PORT"
echo "Service URL: $URL"
