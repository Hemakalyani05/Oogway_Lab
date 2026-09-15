#!/usr/bin/env bash
set -e

echo "============================================================"
echo " Starting The Lenny Growth Assistant (Local Quickstart)     "
echo "============================================================"

# Resolve project directories
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="${PROJECT_ROOT}/backend:${PYTHONPATH}"

# Check if .env exists
if [ ! -f "${PROJECT_ROOT}/.env" ]; then
  echo "Creating .env from .env.example..."
  cp "${PROJECT_ROOT}/.env.example" "${PROJECT_ROOT}/.env"
fi

# Run automated test suite
echo "Running backend test verification..."
python3 -m unittest discover -s "${PROJECT_ROOT}/backend/tests" -p "test_*.py"

echo ""
echo "✅ All tests passed successfully!"
echo "Starting FastAPI backend on http://localhost:8000..."
echo "Swagger API documentation: http://localhost:8000/docs"
echo "Health check endpoint:     http://localhost:8000/healthz"
echo ""

cd "${PROJECT_ROOT}/backend"
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
