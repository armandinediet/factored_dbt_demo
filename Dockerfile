FROM python:3.12-slim

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PROJECT_DIR=/project/dbt
ENV PROFILES_DIR=/project/dbt
ENV DBT_PROJECT_DIR=/project/dbt
ENV DBT_PROFILES_DIR=/project/dbt

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

RUN chmod +x /project/scripts/run_pipeline.sh

CMD ["/project/scripts/run_pipeline.sh"]