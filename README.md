# fast-api-kube API

## Prerequisites

### Docker docker-compose
Install docker and have the daemon running: https://docs.docker.com/get-docker/
### Helm 
Install Helm  https://helm.sh/docs/intro/install/

### Docker registry

## Getting started

- Clone this repo ☝️:

```
     git clone https://github.com/maher-naija-pro/fast-api-kube.git
     cd fast-api-kube.git
```

 - Build the container image :
```
 sudo /scripts/build.sh
```
 - Bring up the container: 

```
 sudo scripts/up.sh
```
 - Check on your browser: <http://localhost:8080/check>
  

## Interactive API docs
Go to http://127.0.0.1:8000/docs.

You will see the automatic interactive API documentation (provided by Swagger UI)

## Configuration

Defaults in this repo. Please change them to suit your needs:

### Python version:
Dockerfile#1: FROM python:3.9

### Image name : `fastapiapp`

docker build -t fastapiapp .
docker-compose.yaml#5      image: fastapiapp:latest

### Image registry : 
values.yaml#10 
### repository:  
mahernaija/fastapi-kube-api:tagname


## Useful command for manual tests

### Activate venv : 
```
env\Scripts\activate
```

### Start  application :
```
fastapi dev src/main.py
```
### Manuel test helm chart
```
helm upgrade --cleanup-on-fail  --install -f fast-api-kube/values.yaml --atomic --timeout 5m fast-api-kube ./fast-api-kube  --version 1.0.0
```
### Manuel push to docker hub

```
 docker login -u mahernaija
 docker tag fastapiapp:latest  mahernaija/fastapiapp:latest
 docker push mahernaija/fastapiapp:latest
```
