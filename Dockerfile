# Use a slim image for a smaller size
FROM python:3.9.20-slim

# Set build argument for environment (default to 'dev')
ARG ENVIRONMENT=dev

# Environment variables for better robustness and security
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 

# Set the maintainer
LABEL maintainer="Maher NAIJA <maher.naija@gmail.com>"

# Set the working directory
WORKDIR /app/

# Start building
RUN echo "I'm building for $ENVIRONMENT"

# Set the working directory
WORKDIR /app/

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
COPY --chown=appuser:appuser ./src /app/

# Copy the entrypoint script
COPY --chown=appuser:appuser ./scripts/entrypoint.sh /app/scripts/

# Make the entrypoint script executable
RUN chmod +x /app/scripts/entrypoint.sh

# Expose the application port
EXPOSE 3000
# Run the pytest command by default
CMD ["pytest", "--maxfail=1", "--disable-warnings", "-v"]
# Set the entrypoint script
#ENTRYPOINT ["/app/scripts/entrypoint.sh"]
