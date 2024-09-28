# Fast API Helm Chart

This Helm chart deploys a FastAPI application on a Kubernetes cluster.

## Prerequisites

- Kubernetes 1.18+
- Helm v3.16.1+


# Production deployment
## Production Install helm chart
- Rename file  value_exemple.yaml value-dev.yaml
- Rename file  value_exemple.yaml value-staging.yaml
- Rename file  value_exemple.yaml value-prod.yaml
```
 cp fast-api-kube-helm/value_exemple.yaml  value-dev.yaml
 cp fast-api-kube-helm/value_exemple.yaml  value-stagging.yaml
 cp fast-api-kube-helm/value_exemple.yaml  value-prod.yaml
```

- Change in value.yaml  env.APP_MODE: "dev" / "prod" / "staging"
- Change in value.yaml  configmaps.db-host configmaps.DB_USER configmaps.DB_PASS 
- Change in value.yaml  db.password-

- Install helm chart on kube:
```
helm install --debug    fast-api-kube ./fast-api-kube-helm -n  fast-api-app --create-namespace
```
## Production check
```
 kubectl get pods -n fast-api-app
 ```

## Production uninstall helm chart
```
helm uninstall --debug    fast-api-kube  -n  fast-api-app

```
## Test helm deployement with helm test
```
helm test   fast-api-kube -n  fast-api-app 
```

## Access production on node port 
```
sh ./scripts/get_url.sh  # It will return URL to access application

```
## Test app in prod
```
curl "URL"
```
NB: Should be changed to ingress depend on cluster architecture

