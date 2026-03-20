{{ config(materialized='table', schema='analytics') }}

select
    cast(o.order_date as date) as order_day,
    p.category,
    count(distinct o.order_id) as total_orders,
    count(distinct o.customer_id) as total_customers,
    sum(oi.quantity) as total_items,
    sum(oi.item_total) as gross_revenue,
    round(sum(oi.item_total) / nullif(count(distinct o.order_id), 0), 2) as average_order_value
from {{ ref('stg_orders') }} as o
left join {{ ref('stg_order_items') }} as oi
    on o.order_id = oi.order_id
left join {{ ref('stg_products') }} as p
    on oi.product_id = p.product_id
where o.order_status not in ('cancelled', 'refunded')
group by 1, 2
order by 1, 2
