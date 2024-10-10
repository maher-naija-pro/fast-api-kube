# Use a slim image for a smaller size
FROM python:3.9.20-slim

# Set build argument for environment (default to 'dev')
ARG ENVIRONMENT=dev

# Environment variables for better robustness and security
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENV=dev

# Set the maintainer
LABEL maintainer="Maher NAIJA <maher.naija@gmail.com>"

# Set the working directory
WORKDIR /app/

# Start building
RUN echo "I'm building for $ENVIRONMENT"

# Install curl
RUN apt-get update && apt-get install -y --no-install-recommends  curl=*  && rm -rf /var/lib/apt/lists/*


# Copy dependency files first to optimize Docker cache
COPY requirements/ /app/requirements/

# Install environment-specific dependencies
RUN set -eux; \
    if [ "$ENVIRONMENT" = "prod" ]; then \
        pip install --no-cache-dir -r /app/requirements/prod.txt; \
    elif [ "$ENVIRONMENT" = "staging" ]; then \
        pip install --no-cache-dir -r /app/requirements/staging.txt; \
    else \
        pip install --no-cache-dir -r /app/requirements/dev.txt; \
    fi

# Create a non-root user for running the container
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser /app
USER appuser

# Copy the application source code
COPY --chown=appuser:appuser ./ /app/

# Add a health check for the application
HEALTHCHECK --interval=1s --timeout=10s --start-period=1s --retries=30 \
    CMD curl --fail http://localhost:3000/health || exit 1

# Expose the application port
EXPOSE  3000

# Run the pytest command by default
CMD ["hypercorn", "src/main:app", "-b", "0.0.0.0:3000", "--reload", "--access-logfile", "-"]

