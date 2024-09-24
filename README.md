# fast-api-kube API

## Prerequisites

### Docker

Install Docker version 27.3.1, build ce12230 and have the daemon running: https://docs.docker.com/engine/install/

### Docker-compose

Install Docker Compose version v2.29.6: https://docs.docker.com/compose/install/standalone/

### Helm

Install Helm https://helm.sh/docs/intro/install/

## Getting started

- Clone this repo ☝️:

```
     git clone https://github.com/maher-naija-pro/fast-api-kube.git
     cd fast-api-kube
```

- Build the container image :

```
 sudo /scripts/build.sh
```

- Rename .env_exemple to .env and set your variable for posgtres database

```
 mv .env_exemple  .env
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
docker-compose.yaml#5 image: fastapiapp:latest

### Image registry :

values.yaml#10

### repository:

mahernaija/fastapi-kube-api:tagname

## Useful command for manual tests

### Activate venv :

```
env\Scripts\activate
```

### Start application :

```
fastapi dev src/main.py
```

### Manuel test helm chart

```
helm upgrade --cleanup-on-fail  --install -f fast-api-kube/values.yaml --atomic --timeout 5m fast-api-kube ./fast-api-kube  --version 1.0.0
```
### Manuel install python dependencies
```
pip install  --no-cache-dir -r ./requirements/dev.txt

```
### Manuel push to docker hub

```
 docker build  --build-arg ENVIRONMENT=dev .
 docker login -u username
 docker tag fastapiapp:latest  username/fastapiapp:latest
 docker push username/fastapiapp:latest
```

# CI/CD
## CI/CD tasks
We use github action for CI/CD to:
 - Check Code Quality with flake8
 - Run tests with pytest
 - Build Docker image and push it to GitHub regitry
 - Security check

## CI/CD Artifacts
CI/CD workflow generate these artifacts:
 - flake8-coverage-report
 - pytest-coverage-report

# Manuel tests
- Run the docker container
```
sudo docker-compose up --build
```

- Run tests on localhost execute bash script

```
./scripts/test.sh

```

# Alembic Database migration

 alembic init migrations
 alembic revision --autogenerate -m "Create a baseline migrations"
 alembic upgrade head
 alembic revision -m "Fill empty "

 # Env vars 
DB_URI
DB_USER=your_user
DB_PASSWORD=your_super_secret_password
DB_NAME=your_db_name


 
# Lint helm charts
 helm lint
# Lint helm charts
helm delete fast-api-kube
# Lint helm charts
helm  history    fast-api-kube
# Test helm charts
 helm install --debug --dry-run    fast-api-kube .
# Install helm charts
 helm install --debug     fast-api-kube ./
#  Check deployement 
kubectl get deployment fast-api-kube -o yaml


helm status    fast-api-kube-2

 1. Get the application URL by running these commands:
 
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=fast-api-kube,app.kubernetes.io/instance=fast-api-kube" -o jsonpath="{.items[0].metadata.name}")
 
  export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
 

# TODO

- Add helm secrets plugin and manage secret gpg encryption or store secret on secret manager
- Add ci to validate docker file  
- Test helm charts release and lint

Please ensure the service starts on port 3000 and your REST API has an access log. Don't forget about graceful shutdowns.


If possible, please make sure that OpenAPI/Swagger is available so we can generate a client for your service (not mandatory). A Loom or YouTube video demonstrating your REST APIs with Swagger would be appreciate

The /v1/tools/lookup endpoint should resolve ONLY the IPv4 addresses for the given domain. Make sure you log all successful queries and their result in a database of your choosing (PostgreSQL, MySQL/MariaDB, MongoDB, Redis, ElasticSearch, SurrealDB, etc.). No SQLite or file-based databases, as we're planning on deploying this service to Kubernetes.

For the /v1/tools/validate endpoint, the service should validate if the input is an IPv4 address or not.

The /v1/history endpoint should retrieve the latest 20 saved queries from the database and display them in order (the most recent should be first).


Rename file  value_exemple.yaml value.yaml
Change in value.yaml  env.APP_MODE: "dev" / "prod" / "staging"
Change in value.yaml  configmaps.db-host configmaps.DB_USER configmaps.DB_PASS 
Change in value.yaml  db.password



# test API
curl http://0.0.0.0:3000/health
curl http://0.0.0.0:3000/
curl http://0.0.0.0:3000/metrics

curl -X POST "http://localhost:3000/v1/tools/validate" \
-H "Content-Type: application/json" \
-d "{\"ip\": \"192.168.1.1\"}"

# Get documentation

 http://127.0.0.1:3000/docs 