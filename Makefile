MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
MYPY_EXCLUDES = --exclude 'venv'
FLAKE8_EXCLUDES = --extend-exclude=venv

build: nginx/certs/server.crt
	docker compose up --build -d

up: nginx/certs/server.crt
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down -v
	
nginx/certs/server.crt:
	mkdir -p nginx/certs
	openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
	-keyout nginx/certs/server.key -out nginx/certs/server.crt \
	-subj "/CN=localhost" -addext "subjectAltName=DNS:localhost"

fclean:
	find . -not -path './venv/*' -type d \( -name "__pycache__" -o -name ".mypy_cache" -o -name ".pytest_cache" \)  -exec rm -rf {} +
	find . -not -path './venv/*' -type f \( -name "*.pyo" -o -name "*.pyc" -o -name "*~" \) -delete

lint:
	uv run python -m flake8 . ${FLAKE8_EXCLUDES}
	uv run python -m mypy . ${MYPY_FLAGS} ${MYPY_EXCLUDES}

.PHONY: build up down clean fclean lint
