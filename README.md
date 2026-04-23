# AE → DE mini demo with dbt, Poetry, Postgres and Makefile

A simple local project to show how a small analytics/data engineering workflow looks in practice:

- Python managed with `pyenv` + `poetry`
- Postgres running in Docker
- Public fake API ingestion for `products` and `customers`
- Local script generation for `orders` and `order_items`
- dbt building `raw -> staging -> marts`
- Makefile commands from the project root

## Architecture

```text
API (products, customers) ─┐
                           ├─> Postgres raw tables ─> dbt staging ─> dbt marts
Python generator (orders) ─┘
```

## Project layout

```text
.
├── Makefile
├── docker-compose.yml
├── .env.example
├── pyproject.toml
├── src/
│   └── ingest/
│       ├── api_ingest.py
│       ├── db.py
│       └── generate_orders.py
└── dbt/
    ├── dbt_project.yml
    ├── profiles.yml
    ├── macros/
    │   └── generate_schema_name.sql
    └── models/
        ├── staging/
        └── marts/
```

## Why these tools matter

### pyenv
Keeps the Python version consistent across machines.

### poetry
Manages dependencies and virtual environments in a reproducible way.

### docker
Lets everyone run the same Postgres locally without manual database installation.

### dbt
Transforms already-loaded data into analytical models with lineage, tests and documentation.

## Quick start

1. Copy env file

```bash
cp .env.example .env
```

2. Start Postgres

```bash
make up
```

3. Install dependencies

```bash
make install
```

4. Ingest fake API data

```bash
make ingest-api
```

5. Generate transactional data

```bash
make generate-orders
```

6. Run dbt

```bash
make dbt-debug
make dbt-run
make dbt-test
```

7. Optional docs

```bash
make dbt-docs
```

## Notes for the demo

- `profiles.yml` and `dbt_project.yml` live inside `dbt/`
- dbt commands are called from the project root
- `PROJECT_DIR` and `PROFILES_DIR` are exported and passed explicitly by the Makefile
- every SQL model includes a top-level `config()` block with `materialized` and `schema`
- `generate_schema_name.sql` is overridden so dbt uses the configured schema directly instead of appending the default target schema

## Example flow

```bash
make up
make install
make ingest-api
make generate-orders
make dbt-run
make dbt-test
```

### ingest commands
```bash
	poetry run python -m src.ingest.api_ingest
	poetry run python -m src.ingest.generate_orders
```


### dbt commands
```bash
poetry run dbt run --project-dir ./dbt --profiles-dir ./dbt
poetry run dbt test --project-dir ./dbt --profiles-dir ./dbt
poetry run dbt seed --project-dir ./dbt --profiles-dir ./dbt
poetry run dbt build --project-dir ./dbt --profiles-dir ./dbt
```