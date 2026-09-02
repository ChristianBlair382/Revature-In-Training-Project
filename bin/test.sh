#!/usr/bin/env bash

# Run with: bash bin/test.sh

set -e

echo "== CASHCOW TESTCASE RUNNER =="

cd backend

if [! -d ".venv"]; then
    echo "Virtual Environment not found. Try running bash bin/setup.sh first."
    exit 1
fi

source .venv/Scripts/activate

DB_EXISTS=$(psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='cashcow_test'")

if [ $DB_EXIST != "1" ]; then
    echo "Testing Database not found. Creating new testing database..."
    psql -U postgres -c "CREATE DATABASE cashcow_test;"
fi

echo "Running tests..."
pytest -v

echo "Test run complete."