#!/usr/bin/env bash
set -e

echo "============================================================"
echo " Starting The Lenny Growth Assistant (Local Quickstart)     "
echo "============================================================"

# Check if .env exists
if [ ! -f .env ]; then
  echo "Creating .env from .env.example..."
  cp .env.example .env
fi

# Run automated test suite
echo "Running backend test verification..."
python3 -m unittest discover -s backend/tests

echo ""
echo "Tests passed! Starting FastAPI backend on http://localhost:8000..."
echo "Swagger API documentation available at http://localhost:8000/docs"
echo ""

cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
