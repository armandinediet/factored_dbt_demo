{{ config(materialized='table', schema='analytics') }}

select
    oi.order_item_id,
    oi.order_id,
    o.customer_id,
    oi.product_id,
    o.order_date,
    o.order_status,
    o.payment_method,
    oi.quantity,
    oi.unit_price,
    oi.item_total
from {{ ref('stg_order_items') }} as oi
left join {{ ref('stg_orders') }} as o
    on oi.order_id = o.order_id
