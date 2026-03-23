
from __future__ import annotations

import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

load_dotenv()


def get_database_url() -> str:
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    dbname = os.getenv("POSTGRES_DB", "analytics")
    user = os.getenv("POSTGRES_USER", "analytics")
    password = os.getenv("POSTGRES_PASSWORD", "analytics")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"


def get_engine() -> Engine:
    return create_engine(get_database_url(), future=True)


@contextmanager
def get_connection():
    engine = get_engine()
    with engine.begin() as connection:
        yield connection


def ensure_raw_schema() -> None:
    with get_connection() as connection:
        connection.execute(text("create schema if not exists raw;"))


def truncate_raw_tables() -> None:
    ensure_raw_schema()
    with get_connection() as connection:
        connection.execute(text("""
            do $$
            begin
                if exists (
                    select 1
                    from information_schema.tables
                    where table_schema = 'raw' and table_name = 'raw_order_items'
                ) then
                    truncate table raw.raw_order_items;
                end if;

                if exists (
                    select 1
                    from information_schema.tables
                    where table_schema = 'raw' and table_name = 'raw_orders'
                ) then
                    truncate table raw.raw_orders;
                end if;

                if exists (
                    select 1
                    from information_schema.tables
                    where table_schema = 'raw' and table_name = 'raw_customers'
                ) then
                    truncate table raw.raw_customers;
                end if;

                if exists (
                    select 1
                    from information_schema.tables
                    where table_schema = 'raw' and table_name = 'raw_products'
                ) then
                    truncate table raw.raw_products;
                end if;
            end
            $$;
        """))