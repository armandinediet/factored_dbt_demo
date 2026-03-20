{{ config(materialized='view', schema='staging') }}

select
    product_id,
    product_name,
    category,
    brand,
    cast(price as numeric(12,2)) as price,
    stock_quantity,
    source_loaded_at
from {{ source('raw', 'raw_products') }}
