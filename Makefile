.PHONY: help setup test backend frontend docker-up docker-down ingest clean

help:
	@echo "The Lenny Growth Assistant - Commands:"
	@echo "  make setup       Install local dependencies"
	@echo "  make test        Run backend test suite"
	@echo "  make backend     Start backend FastAPI server on port 8000"
	@echo "  make frontend    Start frontend dev server on port 5173"
	@echo "  make docker-up   Start full stack (Backend, Frontend, Postgres, Ollama) via Docker"
	@echo "  make docker-down Stop docker stack"
	@echo "  make ingest      Re-index podcast transcripts"

setup:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

test:
	cd backend && python3 -m unittest discover -s tests

backend:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

frontend:
	cd frontend && npm run dev

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

ingest:
	cd backend && python3 -m app.rag.ingest

clean:
	rm -rf backend/*.db backend/__pycache__ frontend/dist
