include .env
export
export DBT_PROFILES_DIR=$(PROFILES_DIR)
export DBT_PROJECT_DIR=$(PROJECT_DIR)
PYTHON := poetry run python


DBT := poetry run dbt

.PHONY: help up down logs install ingest-api generate-orders ingest reset-db dbt-debug dbt-run dbt-test dbt-docs dbt-clean demo
.PHONY: full-run

help:
	@echo "Available commands:"
	@echo "  make up              - start Postgres in Docker"
	@echo "  make down            - stop containers"
	@echo "  make logs            - view Postgres logs"
	@echo "  make install         - install Python dependencies with Poetry"
	@echo "  make ingest-api      - load products and customers from DummyJSON"
	@echo "  make generate-orders - generate fake orders and order_items"
	@echo "  make ingest          - run both ingestion steps"
	@echo "  make reset-db        - recreate raw tables"
	@echo "  make dbt-debug       - validate dbt connection"
	@echo "  make dbt-run         - run dbt models"
	@echo "  make dbt-test        - run dbt tests"
	@echo "  make dbt-docs        - generate dbt docs"
	@echo "  make dbt-clean       - clean dbt target artifacts"
	@echo "  make demo            - install + ingest + dbt run + dbt test"

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f postgres

install:
	poetry install

ingest-api:
	$(PYTHON) -m src.ingest.api_ingest

generate-orders:
	$(PYTHON) -m src.ingest.generate_orders

ingest: ingest-api generate-orders

reset-db:
	$(PYTHON) -m src.ingest.db --reset

dbt-debug:
	$(DBT) debug

dbt-run:
	$(DBT) run

dbt-build:
	$(DBT) build

dbt-test:
	$(DBT) test

dbt-docs:
	$(DBT) docs generate

dbt-serve:
	$(DBT) docs serve

dbt-clean:
	$(DBT) clean

demo: install ingest dbt-run dbt-test

full-run:
	@echo "Starting full pipeline..."
	$(MAKE) ingest-api
	$(MAKE) generate-orders
	$(MAKE) dbt-build
	@echo "Full pipeline finished."

schedule:
	bash scripts/run_pipeline.sh  
	