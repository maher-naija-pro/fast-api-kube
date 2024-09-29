#!/bin/bash
docker-compose down
docker build  --build-arg ENVIRONMENT=dev  --pull --rm -f "Dockerfile" -t fastapiapp:latest "."
docker-compose -f "docker-compose.yml" run test  
