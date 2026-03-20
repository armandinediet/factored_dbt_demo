{{ config(materialized='table', schema='analytics') }}

select
    product_id,
    product_name,
    category,
    brand,
    price,
    stock_quantity
from {{ ref('stg_products') }}
