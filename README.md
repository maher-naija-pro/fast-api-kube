# Fast-api-kube API

## Prerequisites

### Docker

- Install Docker version 27.3.1, build ce12230 and have the daemon running: https://docs.docker.com/engine/install/

### Docker-compose

- Install Docker Compose version v2.29.6: https://docs.docker.com/compose/install/standalone/

### Helm

- Install Helm https://helm.sh/docs/intro/install/

## Getting started for developer

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

- Go to http://127.0.0.1:8000/docs.

- You will see the automatic interactive API documentation (provided by Swagger UI)

## Configuration

- Defaults in this repo. Please change them to suit your needs:

### Python version:
```
Dockerfile#1: FROM python:3.9
```
### Image name : `fastapiapp`
```
docker build -t fastapiapp .
docker-compose.yaml#5 image: fastapiapp:latest
```
### Image registry :
```
values.yaml#10
```
### repository:
```
mahernaija/fastapi-kube-api:tagname
```
## CI/CD
### CI/CD tasks
We use github action for CI/CD to:
 - Check Code Quality with flake8
 - Run tests with pytest
 - Build Docker image and push it to GitHub regitry
 - Security check

### CI/CD Artifacts
CI/CD workflow generate these artifacts:
 - flake8-coverage-report
 - pytest-coverage-report

## tests
- Run the docker container
```
sudo docker-compose up --build
```

- Run tests on localhost execute bash script

```
./scripts/test.sh

```


## Environment Variables

| Variable Name | Description                     | Example Value            |
|---------------|---------------------------------|--------------------------|
| `DB_USER`     | Username for the database       | `admin`                  |
| `DB_PASSWORD` | Password for the database       | `secretpassword`         |
| `DB_NAME`     | Name of the database            | `my_database`            |


## Useful command for manual tests

### Activate venv (windows) :

```
env\Scripts\activate
```

### Manuel Start application :

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

### Manual Alembic Database migration
```
alembic init migrations
alembic revision --autogenerate -m "Create a baseline migrations"
alembic upgrade head
alembic revision -m "Fill empty "
```

###  helm charts useful cmds
```
helm lint
helm delete fast-api-kube
helm  history    fast-api-kube
helm install --debug --dry-run    fast-api-kube .
helm install --debug     fast-api-kube ./
kubectl get deployment fast-api-kube -o yaml
helm status    fast-api-kube
```

# Production deployment

Rename file  value_exemple.yaml value.yaml

- Change in value.yaml  env.APP_MODE: "dev" / "prod" / "staging"
- Change in value.yaml  configmaps.db-host configmaps.DB_USER configmaps.DB_PASS 
- Change in value.yaml  db.password-
- Install helm chart on kube:
```
helm install --debug --dry-run    fast-api-kube ./fast-api-kube-helm/
```

# TODO

- Add helm secrets plugin and manage secret gpg encryption or store secret on secret manager
- Add ci to validate docker file  
- Test helm charts release and lint
- Add  access log
- Close db on shutdown
- Test  /v1/tools/lookup  result
- Test /v1/tools/validate  result 
- Test /v1/history endpoint result
- Add db relation for addresses
- Test docker compose migration  and procedure
- Test kube deployement and procedure




# Test API
```
curl http://0.0.0.0:3000/health
curl http://0.0.0.0:3000/
curl http://0.0.0.0:3000/metrics

curl -X POST "http://localhost:3000/v1/tools/validate" \
-H "Content-Type: application/json" \
-d "{\"ip\": \"192.168.1.1\"}"
```

