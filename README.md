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
| `POSTGRES_USER`     | Username for the database       | `admin`                  |
| `POSTGRES_PASSWORD` | Password for the database       | `secretpassword`         |
| `POSTGRES_NAME`     | Name of the database            | `my_database`            |

## Deep Configuration
### Customizing `Dockerfile`
The `Dockerfile` Below are the default configurations that you may want to adjust based on your specific project needs:

- **Base Image**:
  - Default: `python:3.9.20-slim`
  - You can customize the Python version 

- **Environment**:
  - Default: `ENVIRONMENT=dev`
  - Customize this value to switch between different environments. For example:
    - `dev`: For development environment (includes development dependencies).
    - `staging`: For staging environment.
    - `prod`: For production environment (includes only production dependencies).
  - Modify the default `ENVIRONMENT` by adjusting the `ARG ENVIRONMENT` line in the `Dockerfile`.

- **Application Port**:
  - Default: `3000`
  - This can be customized by changing the `EXPOSE` directive in the `Dockerfile` if your application listens on a different port.

- **Non-Root User**:
  - Default: `appuser`
  - A non-root user is created and used by default for enhanced security. You can modify or remove this by adjusting the `RUN` and `USER` directives in the `Dockerfile` if your application needs specific user permissions.

- **Python Environment Variables**:
  - The following environment variables are set by default to optimize Python behavior in Docker:
    - `PYTHONDONTWRITEBYTECODE=1`: Prevents Python from writing `.pyc` files.
    - `PYTHONUNBUFFERED=1`: Ensures output is sent directly to terminal without being buffered.
  - These can be adjusted or removed based on your specific application needs.

- **Application Entrypoint**:
  - Default command to run the application: 
    ```bash
    hypercorn --reload --log-level info --graceful-timeout 0 src.main:app
    ```
  - Customize this if you use a different server (e.g., `uvicorn`, `gunicorn`) or a different application structure.

### Customizing `docker-compose.yml`



#### 1. **API Service (FastAPI)**
This service runs the FastAPI application using `hypercorn` and applies Alembic migrations during startup.

- **Command**:
  - The default command runs database migrations using `alembic` and starts the API with `hypercorn`. 
    ```bash
    bash -c "alembic upgrade head && hypercorn src/main:app -b 0.0.0.0:3000 --reload --access-logfile - --graceful-timeout 0"
    ```
  - You can modify this command to suit your needs (e.g., changing the entrypoint or server).

- **Develop Mode**:
  - The `develop` section allows live reloading of the source code (`/src/`) and rebuilding when changes are made to `requirements/dev.txt`.
  - You can customize the `watch` paths or actions based on your development workflow.

- **Ports**:
  - Default: `3000:3000`. You can change the exposed ports if your application needs a different one.

- **Resources**:
  - CPU and memory limits are set to ensure the service does not over-consume resources:
    ```yaml
    limits:
      cpus: '1.0'
      memory: 512M
    ```
  - Adjust these limits as needed based on your server's capacity.

#### 2. **Test Service**
This service runs the test suite using `pytest`.

- **Ports**:
  - Default: `4000:3000` to avoid conflict with the API service, but you can modify this as required.

- **Resources**:
  - Similar CPU and memory limits as the `api` service are applied.

- **Image**:
  - The default image is `postgres:12.1-alpine`,You can update the image version or switch to a different database if necessary.

- **Environment Variables**:
  - The PostgreSQL service uses environment variables for configuring the database:
    ```yaml
    POSTGRES_USER
    POSTGRES_PASSWORD
    POSTGRES_DB
    ```
  - These values are loaded from an `.env` file. You can customize them by changing the `.env` file or setting them directly in the `docker-compose.yml` file.

- **Volumes**:
  - The database data is persisted using a named volume (`postgres_data_disk`). You can modify the volume name or path if needed.

- **Resources**:
  - CPU and memory limits are set for this service to ensure the database doesn’t consume excessive resources:
    ```yaml
    limits:
      cpus: '0.5'
      memory: 256M
    ```

### Volumes

- **postgres_data_disk**:  
  - This volume persists the PostgreSQL data, so it's not lost between container restarts. If you need to change the storage location or volume driver, you can do so here.



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
   - Validate docker file
   - pages-build-deployment
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
- Add helm Release to ci 
- Make tests modulars








