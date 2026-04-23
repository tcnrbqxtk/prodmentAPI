.PHONY: be-up be-down be-logs be-shell be-migrate \
        fe-up fe-down fe-logs \
        up down

# ─── Backend ───────────────────────────────────────
be-up:
	docker compose -f backend/docker-compose.yml up -d

be-down:
	docker compose -f backend/docker-compose.yml down

be-logs:
	docker compose -f backend/docker-compose.yml logs -f api

be-shell:
	docker compose -f backend/docker-compose.yml exec api bash

be-migrate:
	docker compose -f backend/docker-compose.yml exec api uv run alembic upgrade head

be-migration:
	docker compose -f backend/docker-compose.yml exec api uv run alembic revision --autogenerate -m "$(name)"

be-build:
	docker compose -f backend/docker-compose.yml build

# ─── Frontend ──────────────────────────────────────
fe-up:
	docker compose -f frontend/docker-compose.yml up -d

fe-down:
	docker compose -f frontend/docker-compose.yml down

fe-logs:
	docker compose -f frontend/docker-compose.yml logs -f frontend

fe-build:
	docker compose -f frontend/docker-compose.yml build

# ─── Together ────────────────────────────────────
up:
	$(MAKE) be-up
	$(MAKE) fe-up

down:
	$(MAKE) be-down
	$(MAKE) fe-down