{{ config(materialized='table', schema='analytics') }}

select
    customer_id,
    first_name,
    last_name,
    email,
    city,
    state,
    country,
    signup_date
from {{ ref('stg_customers') }}
