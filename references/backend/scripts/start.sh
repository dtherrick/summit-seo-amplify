#!/bin/bash
set -e

# Determine environment
if [ "$NODE_ENV" = "development" ]; then
    DEV_FLAG="--dev"
    RELOAD_FLAG="--reload"
    LOG_LEVEL=${LOG_LEVEL:-"debug"}
else
    DEV_FLAG=""
    RELOAD_FLAG=""
    LOG_LEVEL=${LOG_LEVEL:-"info"}
fi

# Convert log level to lowercase for uvicorn compatibility
LOG_LEVEL=$(echo "$LOG_LEVEL" | tr '[:upper:]' '[:lower:]')

# Add current directory to Python path
export PYTHONPATH=/app:$PYTHONPATH

# Run environment validation
echo "Validating environment variables..."
python ./scripts/validate_env.py $DEV_FLAG

# Run database migrations
echo "Running database migrations..."
cd /app && python -m alembic upgrade head

# If validation passes, start the server
echo "Starting server..."
cd /app && exec python -m uvicorn app.main:app \
    --host ${API_HOST:-0.0.0.0} \
    --port ${PORT:-8000} \
    --workers ${WORKERS:-4} \
    --log-level ${LOG_LEVEL} \
    $RELOAD_FLAG 