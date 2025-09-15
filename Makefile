# Simple Makefile

SERVICE := debate-api
PORT ?= 8000

.PHONY: make install test run down clean

make:
	@echo "Available commands:"
	@echo "  make install  - build the Docker image (installs requirements inside the container)"
	@echo "  make test     - run tests inside the container"
	@echo "  make run      - start the service with Docker (and related services)"
	@echo "  make down     - stop all running services"
	@echo "  make clean    - stop and remove containers/images/volumes of the project"

install:
	@if ! command -v docker >/dev/null; then \
		echo "Docker is not installed. Install it from: https://docs.docker.com/get-docker/"; exit 1; \
	fi
	@if ! docker compose version >/dev/null 2>&1; then \
		echo "'docker compose' is not available. Install the plugin: https://docs.docker.com/compose/install/"; exit 1; \
	fi
	docker compose build

test:
	docker compose run --rm $(SERVICE) pytest -q

run:
	docker compose up -d --build
	@echo "API is available at: http://localhost:$(PORT)"

down:
	docker compose down

clean:
	docker compose down -v --rmi local --remove-orphans || true
