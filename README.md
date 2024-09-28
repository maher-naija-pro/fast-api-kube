# Fast-api-kube API

## Branches
There is 3 branches : 

A branch for each stage of deployement:
 - dev
 - stagging
 - prod

## Prerequisites

### Docker

- Install Docker version 27.3.1, build ce12230 and have the daemon running: https://docs.docker.com/engine/install/

### Docker-compose

- Install Docker Compose version v2.29.6: https://docs.docker.com/compose/install/standalone/


## Getting started for developer

- Clone this repo ☝️:

```
git clone https://github.com/maher-naija-pro/fast-api-kube.git
cd fast-api-kube
```

- Build the container image :

```
sh scripts/build.sh
```
or manually execute :
```
docker build  --build-arg ENVIRONMENT=dev  --pull --rm -f "Dockerfile" -t fastapiapp:latest "."
```

- Rename .env_exemple to .env and set your variable for posgtres database

```
mv .env_exemple  .env
```

- Bring up the container:

```
sh scripts/up.sh
```
or manually execute :
```
docker compose down --volumes
docker-compose -f "docker-compose.yml" up -d --build
```
- Check on your browser: <http://localhost:8080/check>
## Tests
- Run the test script
```
sh scripts/test.sh 
```
or manually execute :
```
docker-compose run test
```
## Clean Docker-compose
- Stop docker-compose
```
 sudo docker compose down --volumes
 ```

## Interactive API docs

- Go to http://127.0.0.1:8000/docs

- You will see the automatic interactive API documentation (provided by Swagger UI)

## Environment Variables

| Variable Name | Description                     | Example Value            |
|---------------|---------------------------------|--------------------------|
| `DB_USER`     | Username for the database       | `admin`                  |
| `DB_PASSWORD` | Password for the database       | `secretpassword`         |
| `DB_NAME`     | Name of the database            | `my_database`            |


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
### Repository:
```
mahernaija/fastapi-kube-api:tagname
```

# Production deployment
- For production, you can find under fast-api-kube-helm helm charts to deploy application on Kubernetes 

Please read Readme.md under this directory to deploy on prod step by step


# CI/CD
## CI/CD tasks
- We use github action for CI/CD to:
   - Check Code Quality with flake8
   - Run tests with pytest
   - Build Docker image and push it to GitHub regitry
   - Security check
   - Codacy Static Code Analysis 
   - Lint and check helm charts
   - Release helm charts 
   - Validate docker file

## CI/CD Artifacts
- CI/CD workflow generate these artifacts:
   - flake8-coverage-report
   - pytest-coverage-report

# Python requirement 
- To add a new library to Python there is a requirement directory with a file for each stage of deployement

    - dev.txt
    - prod.txt
    - stagging.txt

# Add an env var: 
To add environment variable to docker and docker-compose update these files: 

- Docker-compose-file:28  => environment:
- Get the env var form python code using:
```
 import os
 ENV_NAME =  os.getenv("ENV_NAME")
```



NB: Fixed version should mbe added


# Useful command for manual tests

## Manual  Test API
```
curl http://0.0.0.0:3000/health
```
```
curl http://0.0.0.0:3000/
```
```
curl http://0.0.0.0:3000/metrics
```
```
curl -X POST "http://localhost:3000/v1/tools/validate" -H "Content-Type: application/json" -d "{\"ip\": \"192.168.1.1\"}"
```
```
curl "http://localhost:3000/v1/tools/lookup?domain=example.com"
```
```
curl "http://localhost:3000/v1/history"
```

## Manuel test helm chart
```
helm upgrade --cleanup-on-fail  --install -f fast-api-kube/values.yaml --atomic --timeout 5m fast-api-kube ./fast-api-kube  --version 1.0.0
```

## Manuel install python dependencies
```
pip install  --no-cache-dir -r ./requirements/dev.txt
```

## Manuel push to docker hub
```
docker build  --build-arg ENVIRONMENT=dev .
docker login -u username
docker tag fastapiapp:latest  username/fastapiapp:latest
docker push username/fastapiapp:latest
```

## Manual Alembic Database migration
```
alembic init migrations
alembic revision --autogenerate -m "Create a baseline migrations"
alembic upgrade head
alembic revision -m "Fill empty "
```

## Lint Docker file :
```
docker run --rm -i hadolint/hadolint < Dockerfile 
```

# TODO

- Add helm secrets plugin and manage secret gpg encryption or store secret on secret manager
- Add ingress rules for production with tls and waf
- Add fast api auth and security
- Connect application to postgres on prod
- Add ARGO CD or flux forCD
- Add helm hooks for alembic migration on prod
- Add helm tests to verify database connection








