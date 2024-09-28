export NODE_PORT=$(kubectl get --namespace fast-api-app  -o jsonpath="{.spec.ports[0].nodePort}" services fast-api-kube)
export NODE_IP=$(kubectl get nodes --namespace fast-api-app -o jsonpath="{.items[0].status.addresses[0].address}")
echo http://$NODE_IP:$NODE_PORT