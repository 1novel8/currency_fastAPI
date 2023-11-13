#!/bin/sh

# exit if error
set -e

# Run migrations
echo "Running application..."

poetry run uvicorn src.app:app --reload --host "$FASTAPI_HOST" --port "$FASTAPI_PORT"
