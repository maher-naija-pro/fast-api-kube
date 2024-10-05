#!/bin/bash


# Exit the script if any command fails
set -e
# Function to log messages with timestamp
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

# Define variables
DOCKER_IMAGE="fastapiapp:latest"
DOCKERFILE="Dockerfile"
DOCKER_COMPOSE_FILE="docker-compose.yml"
ENVIRONMENT="dev"

# Stop and remove containers, networks, images, and volumes
log "Bringing down existing containers..."
docker-compose down || { log "Failed to bring down containers"; exit 1; }

# Build the Docker image with build arguments
log "Building the Docker image..."
docker build \
  --build-arg ENVIRONMENT=$ENVIRONMENT \
  --pull \
  --rm \
  -f "$DOCKERFILE" \
  -t $DOCKER_IMAGE \
  "." || { log "Docker build failed"; exit 1; }

# Run tests using docker-compose
log "Running tests using docker-compose..."
docker-compose -f "$DOCKER_COMPOSE_FILE" run test || { log "Tests failed"; exit 1; }

log "Script completed successfully."
