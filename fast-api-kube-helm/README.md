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

- Change in value.yaml  all variable needed  you can find a complete list below

## Production  install
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

## Values

The following table lists the configurable parameters of the `fast-api-kube` chart and their default values.

| Parameter                                     | Description                                                                                          | Default                             |
|-----------------------------------------------|------------------------------------------------------------------------------------------------------|-------------------------------------|
| `replicaCount`                                | Number of replicas for the FastAPI application                                                        | `3`                                 |
| `image.repository`                            | Container image repository for the application                                                        | `mahernaija/fastapiapp`             |
| `image.pullPolicy`                            | Image pull policy                                                                                     | `IfNotPresent`                      |
| `image.tag`                                   | Image tag to deploy                                                                                   | `latest`                            |
| `imagePullSecrets`                            | Secrets to pull images from private registries                                                        | `[]`                                |
| `nameOverride`                                | Override the chart name                                                                               | `""`                                |
| `fullnameOverride`                            | Override the full name of the chart                                                                   | `""`                                |
| `serviceAccount.create`                       | Specifies whether a service account should be created                                                 | `true`                              |
| `serviceAccount.automount`                    | Automatically mount a ServiceAccount's API credentials                                                 | `true`                              |
| `serviceAccount.annotations`                  | Annotations to add to the service account                                                             | `{}`                                |
| `serviceAccount.name`                         | The name of the service account to use (auto-generated if not provided)                               | `""`                                |
| `podAnnotations`                              | Annotations for the pods                                                                              | `{}`                                |
| `podLabels`                                   | Labels for the pods                                                                                   | `{}`                                |
| `podSecurityContext`                          | Security context for pods                                                                             | `{}`                                |
| `securityContext`                             | Security context for containers                                                                       | `{}`                                |
| `service.type`                                | Kubernetes service type                                                                               | `NodePort`                          |
| `service.port`                                | Kubernetes service port                                                                               | `3000`                              |
| `ingress.enabled`                             | Enable ingress controller                                                                             | `false`                             |
| `ingress.className`                           | Ingress class name                                                                                    | `""`                                |
| `ingress.annotations`                         | Ingress annotations                                                                                   | `{}`                                |
| `ingress.hosts`                               | List of ingress hosts                                                                                 | `[chart-example.local]`             |
| `ingress.tls`                                 | TLS configuration for ingress                                                                         | `[]`                                |
| `resources.limits.cpu`                        | CPU resource limit                                                                                    | `100m`                              |
| `resources.limits.memory`                     | Memory resource limit                                                                                 | `128Mi`                             |
| `resources.requests.cpu`                      | CPU resource request                                                                                  | `100m`                              |
| `resources.requests.memory`                   | Memory resource request                                                                               | `128Mi`                             |
| `livenessProbe.httpGet.path`                  | Path for the liveness probe                                                                           | `/`                                 |
| `livenessProbe.httpGet.port`                  | Port for the liveness probe                                                                           | `http`                              |
| `readinessProbe.httpGet.path`                 | Path for the readiness probe                                                                          | `/`                                 |
| `readinessProbe.httpGet.port`                 | Port for the readiness probe                                                                          | `http`                              |
| `autoscaling.enabled`                         | Enable autoscaling                                                                                    | `false`                             |
| `autoscaling.minReplicas`                     | Minimum number of replicas for autoscaling                                                            | `1`                                 |
| `autoscaling.maxReplicas`                     | Maximum number of replicas for autoscaling                                                            | `1`                                 |
| `autoscaling.targetCPUUtilizationPercentage`  | Target CPU utilization percentage for autoscaling                                                     | `80`                                |
| `autoscaling.targetMemoryUtilizationPercentage`| Target memory utilization percentage for autoscaling                                                  | `80`                                |
| `volumes`                                     | Additional volumes                                                                                    | `[]`                                |
| `volumeMounts`                                | Additional volume mounts                                                                              | `[]`                                |
| `nodeSelector`                                | Node selector                                                                                         | `{}`                                |
| `tolerations`                                 | Tolerations for pod scheduling                                                                        | `[]`                                |
| `affinity`                                    | Affinity rules for pod scheduling                                                                     | `{}`                                |
| `env.LOG_LEVEL`                               | Environment variable for log level                                                                    | `debug`                             |
| `env.APP_MODE`                                | Environment variable for application mode                                                             | `prod`                              |
| `configmaps`                                  | List of config maps for different environments                                                        | `{}`                                |
| `db.password`                                 | Database password                                                                                     | `secretPassword`                    |
