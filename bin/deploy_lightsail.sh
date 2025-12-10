#!/usr/bin/env bash
set -euo pipefail

# Simple workflow to build, push, and deploy to AWS Lightsail Container Service.
# Requirements: docker, aws CLI logged in, and an existing Lightsail container service.

REGION=${REGION:-us-west-2}
SERVICE=${SERVICE:-coffee-canary}
CONTAINER_NAME=${CONTAINER_NAME:-coffee-canary-web-app}
PORT=${PORT:-8050}
DB_URL=${DB_URL:-sqlite:///data/coffee_canary.db}
GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY:-'No Key Found'}
LABEL=${LABEL:-latest}
IMAGE_TAG=coffee-canary:${LABEL}

echo "[1/3] Building image ${IMAGE_TAG} for linux/amd64"
docker buildx build --platform linux/amd64 -t "${IMAGE_TAG}" --load .

echo "[2/3] Pushing image to Lightsail: ${SERVICE}:${LABEL}"
PUSH_OUT=$(aws lightsail push-container-image \
    --region "${REGION}" \
    --service-name "${SERVICE}" \
    --label "${LABEL}" \
    --image "${IMAGE_TAG}")

# Extract the image name from the "Refer to this image as ..." line
IMAGE_NAME=$(printf '%s\n' "$PUSH_OUT" | awk -F'"' '/Refer to this image as/ {print $2}')

echo "[2/3] Using image name: ${IMAGE_NAME}"

echo "[3/3] Creating deployment for service ${SERVICE}"
aws lightsail create-container-service-deployment \
    --region "${REGION}" \
    --service-name "${SERVICE}" \
    --containers "{\"${CONTAINER_NAME}\":{\"image\":\"${IMAGE_NAME}\",\"environment\":{\"DB_URL\":\"${DB_URL}\",\"GOOGLE_MAPS_API_KEY\":\"${GOOGLE_MAPS_API_KEY}\"},\"ports\":{\"${PORT}\":\"HTTP\"}}}" \
    --public-endpoint "containerName=${CONTAINER_NAME},containerPort=${PORT}"

echo "Done."
