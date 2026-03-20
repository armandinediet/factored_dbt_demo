{{ config(materialized='view', schema='staging') }}

select
    order_id,
    customer_id,
    order_date,
    order_status,
    payment_method,
    cast(total_amount as numeric(12,2)) as total_amount,
    source_loaded_at
from {{ source('raw', 'raw_orders') }}
