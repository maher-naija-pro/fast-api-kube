
#!/bin/bash

# Define colors for pretty output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No color

# Function to print a success message
print_success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

# Function to print an error message and exit the script
print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

# Step 1: Stop and remove containers, networks, and volumes
echo "Stopping and removing containers, networks, and volumes..."
docker compose down --volumes
if [ $? -eq 0 ]; then
    print_success "Containers, networks, and volumes stopped and removed."
else
    print_error "Failed to stop and remove containers, networks, or volumes."
fi

# Step 2: Build and start the containers in detached mode
echo "Building and starting containers..."
docker-compose -f "docker-compose.yml" up -d --build
if [ $? -eq 0 ]; then
    print_success "Containers built and started successfully."
else
    print_error "Failed to build and start the containers."
fi

