# Fast-api-kube API
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/maher-naija-pro/fast-api-kube)
![GitHub License](https://img.shields.io/github/license/maher-naija-pro/fast-api-kube)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/maher-naija-pro/fast-api-kube/python-functional-tests.yml)

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
- Check on your browser: <http://localhost:3000/health>
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

## Health Check Endpoint

The `/health` endpoint provides real-time status of the application and its core services, including database. It returns the overall health status, uptime, and latency details.

### Response Example

```json
{
  "status": "healthy",
  "timestamp": "2024-10-10T10:00:00Z",
  "uptime": "02:15:30",
  "version": "1.0.0",
  "services": [
    {"name": "database", "status": "healthy", "latency": 0.123}
  ]
}
```

## Running  Precommit Hooks Manually
To run all hooks manually on all files, you can use:
```
pre-commit run --all-files
```

## Interactive API docs

- Go to http://127.0.0.1:3000/docs

- You will see the automatic interactive API documentation (provided by Swagger UI)

## Logging Configuration

Set the `LOG_LEVEL` environment variable to control log verbosity.
Use `LOG_LEVEL=DEBUG` for detailed logs during development.
Set it with `export LOG_LEVEL=DEBUG` and restart the app to apply changes.
Available levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.


## Environment Variables

### PostgreSQL Configuration

| Variable           | Description                 | Default Value      | Required |
|--------------------|-----------------------------|--------------------|----------|
| `POSTGRES_USER`    | PostgreSQL username         | `appuser`          | Yes      |
| `POSTGRES_PASSWORD`| PostgreSQL password         | `your_secret_password` | Yes   |
| `POSTGRES_DB`      | PostgreSQL database name    | `your_db_name`     | Yes      |
| `POSTGRES_HOST`    | PostgreSQL host             | `db`               | No       |
| `POSTGRES_PORT`    | PostgreSQL port             | `5432`             | No       |

### Rate Limiting Configuration

| Variable              | Description                                      | Default Value | Required |
|-----------------------|--------------------------------------------------|---------------|----------|
| `RATE_LIMIT_REQUESTS` | Maximum number of global requests allowed        | `1000`        | No       |
| `RATE_LIMIT_WINDOW`   | Time window (in seconds) for rate limiting        | `60`          | No       |

### Application Configuration

| Variable      | Description                    | Default Value | Required |
|---------------|--------------------------------|---------------|----------|
| `APP_VERSION` | Application version            | `0.0.1`       | No       |
| `LOG_LEVEL`   | Log level for application logs | `debug`       | No       |
| `APP_PORT`    | Port on which the app runs     | `3000`        | Yes      |

## Deep Configuration
- Check wiki page

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
   - Bandit Static Application Security Testing (SAST)
   - Safety and pip-autdit dependancy scan
   - Checkov helm infra scan
   - Zap owasp scan
   - Auto PR from stagiing to main

## Repository CI/CD Secrets

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
   - zap-report.html

# Python requirement
- To add a new library to Python there is a requirement directory with a file for each stage of deployement

    - dev.txt
    - prod.txt
    - stagging.txt

# Middleware config:

# Security Headers Middleware

This FastAPI application includes a custom middleware called `SecurityHeadersMiddleware` that automatically adds essential **security headers** to every HTTP response. These headers help enhance the security of your application by mitigating common vulnerabilities such as **clickjacking**, **MIME sniffing**, and **cross-site scripting (XSS)**.

## Security Headers Added

The middleware adds the following headers to all responses:
               |
- Check wiki page

## Global rate limiting Middleware
This FastAPI application includes custom middleware to enforce **global rate-limiting**. The rate-limiting middleware is configured using environment variables (requests are limited across all clients).
- Check wiki page

## Control Access Middleware

This FastAPI application includes two essential middlewares for controlling access: **`TrustedHostMiddleware`** and **`CORSMiddleware`**. You can customize their configuration parameters in the `middleware/security_access.py` file, which defines the allowed origins, methods, headers, and hosts for accessing your FastAPI application.

### Configuration Parameters
- Check wiki page

## Manual  Test API
- Check wiki page

# Application Metrics

This repository exposes various application metrics that can be monitored using Prometheus. Below is a breakdown of the metrics and what each one represents.

## Exposed Metrics
- Check wiki page

# Automating Dependency Updates with Dependabot

Dependabot automates dependency updates by checking your project against a database of updates and
security vulnerabilities. Configure it in `.github/dependabot.yml` to run on a daily, weekly, or
monthly schedule. It scans dependency files, identifies outdated versions, and if updates or patches
are available, automatically generates pull requests. These PRs detail changes and potential
compatibility issues, enhancing security and maintaining software quality by keeping dependencies current.


# Pre-Commit Hooks Setup

This project uses pre-commit hooks to automatically ensure that code follows consistent style and quality standards. The hooks are triggered before every commit to check and format Python code using the following tools:
### Tools Used
| **Tool**                 | **Description**                                                                                     |
|--------------------------|-----------------------------------------------------------------------------------------------------|
| **Black**                | Enforces consistent Python code formatting.                                                         |
| **Flake8**               | Checks PEP 8 compliance for clean code.                                                              |
| **Mypy**                 | Static type checker for Python code.                                                                 |
| **Pylint**               | Checks errors and coding standards.                                                                  |
| **Hadolint**             | Lints Dockerfiles following best practices.                                                          |
| **Detect-Secrets**       | Prevents secrets from being committed.                                                               |
| **Pre-commit Hooks**     | Automates checks for code quality.                                                                   |
| **Docker Compose Check** | Validates Docker Compose configurations.                                                             |
| **Helm Lint**            | Ensures Helm charts are structured well.                                                             |
| **Detect Private Key**   | Prevents private keys in commits.                                                                    |
| **Trailing Whitespace**  | Removes trailing whitespaces from lines.                                                             |
| **Check YAML**           | Validates YAML files' format and structure.                                                          |
| **Check JSON**           | Ensures JSON files are formatted correctly.                                                          |
| **Mixed Line Ending**    | Standardizes LF line endings across files.                                                           |
| **Check Large Files**    | Blocks adding large files to repos.                                                                  |

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

- **Add Sphinx Documentation:**
  - Integrate Sphinx for generating project documentation and ensure it's part
    of your CI pipeline for regular updates.

- **Use External Vault for Secrets with Rotation:**
  - Store sensitive information in an external vault (like HashiCorp Vault or
    AWS Secrets Manager) and implement automatic secret rotation.


- **Add Load Testing:**
  - Implement load testing using tools like `Locust` or `k6` to simulate real-
    world traffic and ensure the system scales properly.

- **Add Rollback Functionality for Helm and Alembic Migration:**
  - Implement rollback strategies for both Helm deployments and Alembic
    migrations to handle failed deployments gracefully.

- **Auto increment helm version:**

- **Auto create pr**
- **ADD CHANGELOG.md**
- **ADD CONTRIBUTING.md**
