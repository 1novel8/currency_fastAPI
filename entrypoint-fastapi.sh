#!/bin/sh

# exit if error
set -e

# Run migrations
echo "Running application..."

cd src

poetry run uvicorn main:app --reload --host "$FASTAPI_HOST" --port "$FASTAPI_PORT"
