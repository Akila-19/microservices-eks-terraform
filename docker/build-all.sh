#!/bin/bash

# Set your DockerHub username
DOCKER_USERNAME="akila1908"

# Get version from argument or default to v1
VERSION=${1:-v1}

echo "Building all services with version: $VERSION"

# Build and push user-service
echo "Building user-service..."
docker build -t $DOCKER_USERNAME/user-service:$VERSION ./project/user-service
docker push $DOCKER_USERNAME/user-service:$VERSION

# Build and push product-service
echo "Building product-service..."
docker build -t $DOCKER_USERNAME/product-service:$VERSION ./project/product-service
docker push $DOCKER_USERNAME/product-service:$VERSION

# Build and push api-gateway
echo "Building api-gateway..."
docker build -t $DOCKER_USERNAME/api-gateway:$VERSION ./project/api-gateway
docker push $DOCKER_USERNAME/api-gateway:$VERSION

# Build and push frontend
echo "Building frontend..."
docker build -t $DOCKER_USERNAME/frontend:$VERSION ./project/frontend
docker push $DOCKER_USERNAME/frontend:$VERSION

echo "Done! All images pushed with version: $VERSION"