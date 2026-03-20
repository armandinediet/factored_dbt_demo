{{ config(materialized='view', schema='staging') }}

select
    order_item_id,
    order_id,
    product_id,
    quantity,
    cast(unit_price as numeric(12,2)) as unit_price,
    cast(item_total as numeric(12,2)) as item_total,
    source_loaded_at
from {{ source('raw', 'raw_order_items') }}
