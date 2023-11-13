#!/bin/sh

# exit if error
set -e

# Run celery worker
echo "Running celery worker..."

poetry run python -m celery -A src.celery_tasks worker --loglevel=info
