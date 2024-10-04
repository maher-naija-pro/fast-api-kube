# Fast-api-kube API
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/maher-naija-pro/fast-api-kube)
![GitHub License](https://img.shields.io/github/license/maher-naija-pro/fast-api-kube)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/maher-naija-pro/fast-api-kube/tests.yml)

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

### hadolint
- Downolad hadolint for your platfrom  from  https://github.com/hadolint/hadolint/releases/

for linux: 
```
 sudo wget https://github.com/hadolint/hadolint/releases/download/v2.12.1-beta/hadolint-Linux-x86_64 -O /bin/hadolint
 sudo chmod +x /bin/hadolint
 ```

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

| Variable Name         | Description                                                  | Default Value    | Mandatory / Optional |
|-----------------------|--------------------------------------------------------------|------------------|----------------------|
| `POSTGRES_USER`        | Username for the PostgreSQL database.                        | `admin`          | Mandatory             |
| `POSTGRES_PASSWORD`    | Password for the PostgreSQL database.                        | `secretpassword` | Mandatory             |
| `POSTGRES_NAME`        | Name of the PostgreSQL database.                             | `my_database`    | Mandatory             |
| `RATE_LIMIT_REQUESTS`  | Maximum number of requests allowed within the time window.   | `100`            | Optional              |
| `RATE_LIMIT_WINDOW`    | Time window (in seconds) for rate limiting requests.         | `60`             | Optional              |
| `RETRY_LIMIT`          | Maximum number of retries allowed for failed requests.       | `60`             | Optional              |

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


The `docker-compose.yml` file in this repository is designed to set up and manage multiple services, including the FastAPI API service, a PostgreSQL database, and a test service. Below are the default configurations that can be customized to suit your specific project requirements.

### API Service (FastAPI)

1. **Build Context**:
   The `api` service is built using the `Dockerfile` in the root directory.
   - Default: `context: .`, `dockerfile: Dockerfile`
   - You can modify the build context or Dockerfile location as needed.

2. **Command**:
   The default command runs database migrations using `alembic` and starts the API with `hypercorn`.
   - Default:
     ```bash
     bash -c "alembic upgrade head && hypercorn src/main:app -b 0.0.0.0:3000 --reload --access-logfile - --graceful-timeout 0"
     ```
   - You can modify this command to suit your needs (e.g., changing the entrypoint or server).

3. **Develop Mode**:
   The `develop` section allows live reloading of the source code (`/src/`) and rebuilding when changes are made to `requirements/dev.txt`.
   - Default:
     ```yaml
     watch:
       - action: sync
         path: ./src/
         target: /app/src/
       - action: rebuild
         path: requirements/dev.txt
     ```
   - Customize the `watch` paths or actions based on your development workflow.

4. **Ports**:
   The default exposed port is `3000`.
   - Default: `3000:3000`
   - You can change the exposed ports if your application needs a different one.

5. **Volumes**:
   A bind mount is used to link the source code on your host machine to the `/app` directory in the container.
   - Default:
     ```yaml
     volumes:
       - type: bind
         source: .
         target: /app/
     ```
   - Modify the source or target paths based on your project structure.

6. **Environment Variables**:
   The database connection string is provided through environment variables.
   - Default: `DB_URI=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db/${POSTGRES_DB}`
   - You can change this environment variable to connect to different databases or use other database drivers.

7. **Resources**:
   CPU and memory limits are set to ensure the service does not over-consume resources.
   - Default:
     ```yaml
     limits:
       cpus: '1.0'
       memory: 512M
     ```
   - Adjust these limits as needed based on your server's capacity.

### Test Service

1. **Build Context**:
   Similar to the `api` service, it builds from the same `Dockerfile`.
   - Default: `context: .`, `dockerfile: Dockerfile`
   - Modify if the Dockerfile is located elsewhere.

2. **Command**:
   The default command runs Alembic migrations and executes tests using `pytest`.
   - Default:
     ```bash
     bash -c "alembic upgrade head && pytest"
     ```
   - Customize this if your testing setup differs.

3. **Ports**:
   The test service is exposed on port `4000` to avoid conflict with the API service.
   - Default: `4000:3000`
   - You can adjust the port mappings.

4. **Volumes**:
   A bind mount is used to link the source code on your host machine to the `/app` directory in the container, similar to the API service.
   - Default:
     ```yaml
     volumes:
       - type: bind
         source: .
         target: /app/
     ```
   - Modify the source or target paths based on your project structure.

5. **Resources**:
   CPU and memory limits are set to ensure the service does not over-consume resources.
   - Default:
     ```yaml
     limits:
       cpus: '1.0'
       memory: 512M
     ```
   - Adjust these limits as needed.

### Database Service (PostgreSQL)

1. **Image**:
   The default image is `postgres:12.1-alpine`, which is a lightweight version of PostgreSQL.
   - Default: `postgres:12.1-alpine`
   - You can update the image version or switch to a different database if necessary.

2. **Environment Variables**:
   The PostgreSQL service uses environment variables for configuring the database.
   - Default:
     ```yaml
     environment:
       - POSTGRES_USER
       - POSTGRES_PASSWORD
       - POSTGRES_DB
     ```
   - These values are loaded from an `.env` file. Customize them by changing the `.env` file or setting them directly in the `docker-compose.yml` file.

3. **Volumes**:
   The database data is persisted using a named volume (`postgres_data_disk`).
   - Default:
     ```yaml
     volumes:
       - postgres_data_disk:/var/lib/postgresql/data/
     ```
   - You can modify the volume name or path if needed.

4. **Resources**:
   CPU and memory limits are set for this service to ensure the database doesn’t consume excessive resources.
   - Default:
     ```yaml
     limits:
       cpus: '0.5'
       memory: 256M
     ```
   - Customize this based on your database's performance needs.

### Networks

1. **app_network**:
   All services communicate over a custom bridge network (`app_network`).
   - Default:
     ```yaml
     networks:
       app_network:
         driver: bridge
     ```
   - You can add other services to this network or change the network driver if needed.

### Volumes

1. **postgres_data_disk**:
   This volume is used to persist PostgreSQL data.
   - Default:
     ```yaml
     volumes:
       postgres_data_disk:
         driver: local
     ```
   - You can modify the volume driver or name as needed.

# Production deployment
- For production, you can find under fast-api-kube-helm helm charts to deploy application on Kubernetes

### Please read the [**Readme.md**](https://github.com/maher-naija-pro/fast-api-kube/blob/dev/fast-api-kube-helm/README.md) in this directory for detailed **step-by-step** instructions on deploying this project in a **production** environment.

# CI/CD
## CI/CD tasks
- We use github action for CI/CD to:
   - Check Code Quality with flake8
   - Run tests with pytest
   - Build Docker image and push it to GitHub regitry
   - Build py package and publish it to pypi.org
   - Codacy Static Code Analysis
   - Lint and check helm charts
   - Validate docker file
   - Pages-build-deployment
   - Pycharm Python security scanner
   - Trivy docker image vulnerability scanning tools
   - Bandit Static Application Security Testing (SAST)   security scanner

## Repository Secrets

These secrets are used for automating the CI/CD pipeline and managing external integrations such as Docker Hub, PostgreSQL, and PyPI.

### Setting Up Secrets in GitHub Actions

To configure the required secrets in your repository:

1. Go to your repository on GitHub.
2. Click on the `Settings` tab.
3. In the left sidebar, navigate to **Secrets and variables** > **Actions**.
4. Click **New repository secret**.
5. Enter the **Name** and **Value** for each secret (as shown in the table below).
6. Click **Add secret**.

### Secrets Table

| Secret Name        | Description                                  | Example                      |
|--------------------|----------------------------------------------|------------------------------|
| `DOCKER_PASSWORD`   | Docker Hub password                          | `my-docker-password`          |
| `DOCKER_USERNAME`   | Docker Hub username                          | `my-docker-username`          |
| `POSTGRES_DB`       | PostgreSQL database name                     | `my_database`                |
| `POSTGRES_PASSWORD` | PostgreSQL password                          | `my-postgres-password`        |
| `POSTGRES_USER`     | PostgreSQL username                          | `my-postgres-user`            |
| `PYPI_API_TOKEN`    | API token for uploading packages to PyPI     | `pypi-12345-abcde-token`      |


## CI/CD Artifacts
- CI/CD workflow generate these artifacts:
   - flake8-coverage-report
   - pytest-coverage-report
   - bandit-findings-report

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
# Middleware config:

# Security Headers Middleware

This FastAPI application includes a custom middleware called `SecurityHeadersMiddleware` that automatically adds essential **security headers** to every HTTP response. These headers help enhance the security of your application by mitigating common vulnerabilities such as **clickjacking**, **MIME sniffing**, and **cross-site scripting (XSS)**.

## Security Headers Added

The middleware adds the following headers to all responses:

| **Header**                    | **Description**                                                                                                                                                     | **Example Value**                                                          |
|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| `Strict-Transport-Security`    | Enforces the use of HTTPS and tells the browser to only interact with the site over HTTPS for a specified time period. Also applies the rule to all subdomains.       | `max-age=31536000; includeSubDomains`                                      |
| `X-Content-Type-Options`       | Prevents browsers from MIME-sniffing the content-type of responses, reducing the risk of some types of attacks, such as XSS.                                         | `nosniff`                                                                  |
| `X-Frame-Options`              | Protects against **clickjacking** by preventing the page from being embedded in an iframe.                                                                            | `DENY`                                                                     |
| `X-XSS-Protection`             | Enables the browser’s built-in cross-site scripting (XSS) protection to prevent some forms of XSS attacks.                                                           | `1; mode=block`                                                            |
| `Content-Security-Policy`      | Defines which content sources are allowed to load. Helps prevent XSS by restricting allowed scripts and resources.                                                    | `default-src 'self'; script-src 'self'; object-src 'none'`                 |


## Global rate limiting Middleware
This FastAPI application includes custom middleware to enforce **global rate-limiting**. The rate-limiting middleware is configured using environment variables (requests are limited across all clients).


| Environment Variable    | Description                                         | Default Value |
|-------------------------|-----------------------------------------------------|---------------|
| `RATE_LIMIT_REQUESTS`    | Maximum number of global requests allowed in the time window. If the total number of requests exceeds this limit, subsequent requests will receive a `429 Too Many Requests` response. | `100`         |
| `RATE_LIMIT_WINDOW`      | The time window (in seconds) during which the maximum number of requests is counted. Once the time window expires, the counter resets. | `60`          |

## Control Access Middleware

This FastAPI application includes two essential middlewares for controlling access: **`TrustedHostMiddleware`** and **`CORSMiddleware`**. You can customize their configuration parameters in the `middleware/security_access.py` file, which defines the allowed origins, methods, headers, and hosts for accessing your FastAPI application.

### Configuration Parameters

The following table outlines the configurable parameters for the `CORSMiddleware` and `TrustedHostMiddleware` used in this FastAPI application:

| Parameter                | Middleware             | Description                                                                                     | Default Value              | Recommended Value for Production         |
|--------------------------|------------------------|-------------------------------------------------------------------------------------------------|----------------------------|------------------------------------------|
| `allow_origins`           | `CORSMiddleware`       | Defines which domains are allowed to make requests to the API.                                   | `["*"]`                    | List of trusted domains, e.g., `["https://example.com"]` |
| `allow_methods`           | `CORSMiddleware`       | Specifies the allowed HTTP methods (GET, POST, PUT, etc.).                                       | `["*"]`                    | Restrict to required methods, e.g., `["GET", "POST"]`    |
| `allow_headers`           | `CORSMiddleware`       | Controls which headers are allowed in the requests.                                              | `["*"]`                    | Specify required headers, e.g., `["Authorization", "Content-Type"]` |
| `allow_credentials`       | `CORSMiddleware`       | Allows cookies or authentication credentials to be included in the requests.                     | `True`                     | `True` (if using cookies or credentials)                |
| `allowed_hosts`           | `TrustedHostMiddleware`| Limits the hosts that can access the API.                                                        | `["*", "localhost"]`        | List of trusted hosts, e.g., `["example.com"]` |


### Notes:

- **`allow_origins`**: Setting `["*"]` (allow all origins) is insecure in production environments, as it permits requests from any domain. For production, restrict this to specific trusted domains like `["https://example.com"]`.
- **`allow_methods`**: While `["*"]` allows all HTTP methods, it is recommended to restrict this to only the required methods for your API, such as `["GET", "POST"]`.
- **`allowed_hosts`**: Allowing all hosts with `["*"]` is insecure for production environments. Restrict access to specific trusted hosts, such as `["example.com"]` or `["api.example.com"]`.
- **`allow_credentials`**: Set this to `True` if your API uses cookies or authentication tokens that require credentials to be sent across domains.
- **`allow_headers`**: While `["*"]` allows all headers, you should explicitly specify the headers that are required for your application, such as `["Authorization", "Content-Type"]`.

Make sure to update these parameters in `middleware/security.py` for a production setup to enhance security.


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
# Application Metrics

This repository exposes various application metrics that can be monitored using Prometheus. Below is a breakdown of the metrics and what each one represents.

## Exposed Metrics

| **Metric**                              | **Description**                                                                      | **Labels**                            | **Type**   | **Example**                                                                                     |
|-----------------------------------------|--------------------------------------------------------------------------------------|---------------------------------------|------------|-------------------------------------------------------------------------------------------------|
| `metric_app_requests_total`             | Total number of requests received by the `/metrics` endpoint.                         | None                                  | Counter    | `metric_app_requests_total 1.0`                                                                |
| `metric_app_requests_created`           | Timestamp of the first request on the `/metrics` endpoint since Unix epoch.           | None                                  | Gauge      | `metric_app_requests_created 1.7276320847868874e+09`                                           |
| `metric_app_request_errors_total`       | Total number of request errors encountered on the `/metrics` endpoint.                | None                                  | Counter    | `metric_app_request_errors_total 0.0`                                                          |
| `metric_app_request_errors_created`     | Timestamp of the first request error on the `/metrics` endpoint since Unix epoch.     | None                                  | Gauge      | `metric_app_request_errors_created 1.7276320847869053e+09`                                     |
| `metric_app_request_latency_seconds`    | Request latency in seconds on the `/metrics` endpoint, split into histogram buckets.  | `le`: Latency bucket (e.g., 0.005s, 0.01s, etc.) | Histogram | `metric_app_request_latency_seconds_bucket{le="0.005"} 0.0`<br>`metric_app_request_latency_seconds_bucket{le="0.01"} 0.0` |
| `metric_app_request_latency_seconds_created` | Timestamp of first latency measurement on the `/metrics` endpoint.                 | None                                  | Gauge      | `metric_app_request_latency_seconds_created 1.727632084786929e+09`                             |
| `validate_app_requests_total`           | Total number of requests received on the `/validate` endpoint.                        | None                                  | Counter    | `validate_app_requests_total 0.0`                                                              |
| `validate_app_requests_created`         | Timestamp of the first request on the `/validate` endpoint since Unix epoch.          | None                                  | Gauge      | `validate_app_requests_created 1.727632084825792e+09`                                          |
| `validate_request_duration_seconds`     | Duration of requests on the `/validate` endpoint, split into histogram buckets.       | `le`: Latency bucket (e.g., 0.005s, 0.01s, etc.) | Histogram | `validate_request_duration_seconds_bucket{le="0.005"} 0.0`<br>`validate_request_duration_seconds_bucket{le="0.01"} 0.0` |
| `validate_request_duration_seconds_created` | Timestamp of first duration measurement for `/validate` requests.                   | None                                  | Gauge      | `validate_request_duration_seconds_created 1.7276320848258443e+09`                             |
| `lookup_request_duration_seconds`       | Duration of requests on the `/lookup` endpoint, split into histogram buckets.         | `le`: Latency bucket (e.g., 0.005s, 0.01s, etc.) | Histogram | `lookup_request_duration_seconds_bucket{le="0.005"} 0.0`<br>`lookup_request_duration_seconds_bucket{le="0.01"} 0.0` |
| `lookup_request_duration_seconds_created`| Timestamp of first duration measurement for `/lookup` requests.                     | None                                  | Gauge      | `lookup_request_duration_seconds_created 1.727632084826711e+09`                                |
| `lookup_app_requests_total`             | Total number of requests received on the `/lookup` endpoint.                          | None                                  | Counter    | `lookup_app_requests_total 0.0`                                                                |
| `lookup_app_requests_created`           | Timestamp of the first request on the `/lookup` endpoint since Unix epoch.            | None                                  | Gauge      | `lookup_app_requests_created 1.727632084826785e+09`                                            |
| `history_app_requests_total`            | Total number of requests received on the `/history` endpoint.                         | None                                  | Counter    | `history_app_requests_total 1.0`                                                               |
| `history_app_requests_created`          | Timestamp of the first request on the `/history` endpoint since Unix epoch.           | None                                  | Gauge      | `history_app_requests_created 1.727632084837052e+09`                                           |
| `history_app_request_errors_total`      | Total number of request errors encountered on the `/history` endpoint.                | None                                  | Counter    | `history_app_request_errors_total 0.0`                                                         |
| `history_app_request_errors_created`    | Timestamp of the first request error on the `/history` endpoint since Unix epoch.     | None                                  | Gauge      | `history_app_request_errors_created 1.7276320848370783e+09`                                    |
| `history_app_request_latency_seconds`   | Request latency in seconds on the `/history` endpoint, split into histogram buckets.  | `le`: Latency bucket (e.g., 0.005s, 0.01s, etc.) | Histogram | `history_app_request_latency_seconds_bucket{le="0.005"} 0.0`<br>`history_app_request_latency_seconds_bucket{le="0.01"} 1.0` |
| `root_app_requests_total`               | Total number of requests received on the `/` (root) endpoint.                         | None                                  | Counter    | `root_app_requests_total 0.0`                                                                  |
| `root_app_requests_created`             | Timestamp of the first request on the `/` (root) endpoint since Unix epoch.           | None                                  | Gauge      | `root_app_requests_created 1.727632084847543e+09`                                              |
| `root_app_request_errors_total`         | Total number of request errors encountered on the `/` (root) endpoint.                | None                                  | Counter    | `root_app_request_errors_total 0.0`                                                            |
| `root_app_request_errors_cre  ated`       | Timestamp of the first request error on the `/` (root) endpoint since Unix epoch.     | None                                  | Gauge      | `root_app_request_errors_created 1.727632084847571e+09`                                        |

# Pre-Commit Hooks Setup

This project uses pre-commit hooks to automatically ensure that code follows consistent style and quality standards. The hooks are triggered before every commit to check and format Python code using the following tools:
### Tools Used

1. **Black** - Python code formatter
2. **Flake8** - Python code linting
3. **Pylint** - Advanced Python linting
4. **Hadolint** - Dockerfile linting
5. **Detect-Secrets** - Detecting and preventing secret leaks in code

## How it Works

- Every time you commit code, these tools run automatically, ensuring that the code is formatted and free of common issues before being committed.
- If any problems are detected, the commit is rejected, and you are prompted to fix the issues.


# License

This project is licensed under the MIT License.

# TODO

- **Add Helm Secrets Plugin and manage secret encryption:**
  - Install the [Helm Secrets Plugin](https://github.com/jkroepke/helm-secrets).
  - Use `sops` with GPG for encrypting secrets or integrate with a secret 
    management solution like AWS Secrets Manager or HashiCorp Vault.

- **Add Ingress Rules for Production with TLS and WAF:**
  - Configure ingress rules with TLS support using Cert-Manager for automatic 
    certificate provisioning.
  - Integrate a WAF (e.g., AWS WAF, GCP Cloud Armor) or use NGINX Ingress with 
    ModSecurity for enhanced security.

- **Add Authentication and Security to FastAPI:**
  - Implement OAuth2 with JWT for secure user authentication using FastAPI's 
    built-in support.
  - Add role-based access control (RBAC) for fine-grained permission handling.

- **Connect the Application to PostgreSQL in Production:**
  - Ensure the FastAPI app is connected to a managed PostgreSQL instance in your 
    production environment using environment variables for connection strings.

- **Integrate ArgoCD or Flux for Continuous Delivery (CD):**
  - Set up ArgoCD or Flux to manage GitOps-based continuous delivery for your 
    Kubernetes deployments.

- **Add Helm Hooks for Alembic Database Migrations in Production:**
  - Use Helm post-deploy hooks to trigger Alembic migrations automatically after 
    successful deployments.

- **Add Helm Tests Hook to Verify Database Connection:**
  - Create Helm test hooks to validate the connection between the FastAPI app 
    and the PostgreSQL database after deployment.

- **Add Helm Release to CI Pipeline:**
  - Integrate Helm release steps in your CI pipeline to automatically deploy 
    changes to your Kubernetes cluster.

- **Implement Authentication (OAuth2/JWT):**
  - Set up OAuth2 with JWT tokens for secure access control within your FastAPI 
    application.

- **Implement Role-Based Access Control (RBAC):**
  - Define and enforce role-based permissions within the FastAPI application to 
    ensure proper access control.

- **Test Horizontal Pod Autoscaling (HPA):**
  - Configure and test Kubernetes HPA to automatically scale your application 
    based on CPU or memory usage.

- **Test Multi-Stage Builds:**
  - Optimize Docker builds with multi-stage builds to reduce image size and 
    improve build efficiency.

- **Mock External Dependencies for Testing:**
  - Use tools like `pytest-mock` or custom mock services to simulate external 
    dependencies during unit and integration tests.

- **Set up CI to Regularly Update Dependencies:**
  - Automate dependency updates in your CI pipeline using tools like Dependabot 
    or Renovate to ensure packages stay up-to-date.

- **Add Sphinx Documentation:**
  - Integrate Sphinx for generating project documentation and ensure it's part 
    of your CI pipeline for regular updates.

- **Use External Vault for Secrets with Rotation:**
  - Store sensitive information in an external vault (like HashiCorp Vault or 
    AWS Secrets Manager) and implement automatic secret rotation.

- **Add Static Application Security Testing (SAST):**
  - Integrate a SAST tool (like Bandit or SonarQube) into your CI pipeline to 
    scan for security vulnerabilities in the codebase.

- **Add Dependency Vulnerability Scanning:**
  - Use tools like `safety` or `pip-audit` in the CI pipeline to detect and 
    address vulnerabilities in Python dependencies.

- **Add Load Testing:**
  - Implement load testing using tools like `Locust` or `k6` to simulate real-
    world traffic and ensure the system scales properly.

- **Add Rollback Functionality for Helm and Alembic Migration:**
  - Implement rollback strategies for both Helm deployments and Alembic 
    migrations to handle failed deployments gracefully.



