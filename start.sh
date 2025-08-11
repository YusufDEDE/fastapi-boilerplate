#!/bin/sh

# set -e

# host="${POSTGRES_HOST:-db}"
# port="${POSTGRES_PORT:-5432}"

# echo "Waiting for Postgres at $host:$port..."

# while ! nc -z "$host" "$port"; do
#   echo "Postgres is unavailable - sleeping"
#   sleep 1
# done

# echo "Postgres is up - starting FastAPI app"

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
