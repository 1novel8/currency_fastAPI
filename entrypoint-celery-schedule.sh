#!/bin/sh

# exit if error
set -e

# Run celery schedule
echo "Running celery schedule..."

poetry run python -m celery -A src.celery_tasks beat --loglevel=info
