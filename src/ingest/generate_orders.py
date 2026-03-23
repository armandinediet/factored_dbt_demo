
from __future__ import annotations

import random
from datetime import datetime

import pandas as pd
from faker import Faker
from sqlalchemy import text

from src.ingest.db import get_connection, get_engine

faker = Faker()
random.seed(42)
Faker.seed(42)

ORDER_STATUSES = ["placed", "paid", "cancelled", "refunded"]
PAYMENT_METHODS = ["credit_card", "pix", "debit_card", "paypal"]


def fetch_reference_data() -> tuple[list[int], list[tuple[int, float]]]:
    with get_connection() as connection:
        customer_rows = connection.execute(text("select customer_id from raw.raw_customers order by customer_id"))
        product_rows = connection.execute(text("select product_id, price from raw.raw_products order by product_id"))
        customer_ids = [row[0] for row in customer_rows.fetchall()]
        products = [(row[0], float(row[1])) for row in product_rows.fetchall()]
    return customer_ids, products


def generate_orders_data(num_orders: int = 200) -> tuple[pd.DataFrame, pd.DataFrame]:
    customer_ids, products = fetch_reference_data()
    if not customer_ids or not products:
        raise ValueError("Reference data not found. Run API ingestion first.")

    orders = []
    order_items = []
    next_order_item_id = 1
    load_ts = datetime.utcnow()

    for order_id in range(1, num_orders + 1):
        customer_id = random.choice(customer_ids)
        order_date = faker.date_time_between(start_date="-120d", end_date="now")
        status = random.choices(ORDER_STATUSES, weights=[10, 75, 10, 5], k=1)[0]
        payment_method = random.choice(PAYMENT_METHODS)
        item_count = random.randint(1, 4)
        selected_products = random.sample(products, k=item_count)

        total_amount = 0.0
        for product_id, base_price in selected_products:
            quantity = random.randint(1, 3)
            unit_price = round(base_price, 2)
            item_total = round(quantity * unit_price, 2)
            total_amount += item_total
            order_items.append(
                {
                    "order_item_id": next_order_item_id,
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "item_total": item_total,
                    "source_loaded_at": load_ts,
                }
            )
            next_order_item_id += 1

        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "order_date": order_date,
                "order_status": status,
                "payment_method": payment_method,
                "total_amount": round(total_amount, 2),
                "source_loaded_at": load_ts,
            }
        )

    return pd.DataFrame(orders), pd.DataFrame(order_items)


def load_orders(num_orders: int = 200) -> None:
    orders_df, order_items_df = generate_orders_data(num_orders=num_orders)
    engine = get_engine()

    with get_connection() as connection:
        connection.execute(text("""
            do $$
            begin
                if to_regclass('raw.raw_order_items') is not null then
                    truncate table raw.raw_order_items;
                end if;

                if to_regclass('raw.raw_orders') is not null then
                    truncate table raw.raw_orders;
                end if;
            end
            $$;
        """))

    orders_df.to_sql("raw_orders", engine, schema="raw", if_exists="append", index=False)
    order_items_df.to_sql("raw_order_items", engine, schema="raw", if_exists="append", index=False)

    print(f"Generated {len(orders_df)} orders and {len(order_items_df)} order items.")


if __name__ == "__main__":
    load_orders()
