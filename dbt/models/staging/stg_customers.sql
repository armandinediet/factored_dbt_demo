{{ config(materialized='view', schema='staging') }}

select
    customer_id,
    first_name,
    last_name,
    email,
    city,
    state,
    country,
    signup_date,
    source_loaded_at
from {{ source('raw', 'raw_customers') }}
