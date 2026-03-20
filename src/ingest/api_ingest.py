
from __future__ import annotations

import os
from datetime import datetime

import pandas as pd
import requests
from dateutil import parser
from dotenv import load_dotenv

from src.ingest.db import ensure_raw_schema, get_engine, truncate_raw_tables

load_dotenv()

BASE_URL = os.getenv("DUMMYJSON_BASE_URL", "https://dummyjson.com")


def fetch_products() -> list[dict]:
    response = requests.get(f"{BASE_URL}/products?limit=100", timeout=30)
    response.raise_for_status()
    return response.json().get("products", [])


def fetch_customers() -> list[dict]:
    response = requests.get(f"{BASE_URL}/users?limit=100", timeout=30)
    response.raise_for_status()
    return response.json().get("users", [])


def parse_date(value: str | None):
    if not value:
        return None
    try:
        return parser.parse(value).date()
    except Exception:
        return None


def products_to_dataframe(products: list[dict]) -> pd.DataFrame:
    rows = [
        {
            "product_id": product["id"],
            "product_name": product["title"],
            "category": product.get("category"),
            "brand": product.get("brand"),
            "price": product.get("price"),
            "stock_quantity": product.get("stock"),
            "source_loaded_at": datetime.utcnow(),
        }
        for product in products
    ]
    return pd.DataFrame(rows)


def customers_to_dataframe(customers: list[dict]) -> pd.DataFrame:
    rows = []
    for customer in customers:
        address = customer.get("address") or {}
        rows.append(
            {
                "customer_id": customer["id"],
                "first_name": customer.get("firstName"),
                "last_name": customer.get("lastName"),
                "email": customer.get("email"),
                "city": address.get("city"),
                "state": address.get("state"),
                "country": address.get("country"),
                "signup_date": parse_date(customer.get("birthDate")),
                "source_loaded_at": datetime.utcnow(),
            }
        )
    return pd.DataFrame(rows)


def load_reference_data() -> None:
    products = fetch_products()
    customers = fetch_customers()

    products_df = products_to_dataframe(products)
    customers_df = customers_to_dataframe(customers)

    ensure_raw_schema()
    truncate_raw_tables()

    engine = get_engine()
    products_df.to_sql("raw_products", engine, schema="raw", if_exists="append", index=False)
    customers_df.to_sql("raw_customers", engine, schema="raw", if_exists="append", index=False)

    print(f"Loaded {len(products_df)} products and {len(customers_df)} customers into raw schema.")


if __name__ == "__main__":
    load_reference_data()
