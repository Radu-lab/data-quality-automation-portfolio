SELECT 
    customer_id,
    count(*) as orders,
    sum(amount) as total_income
    from {{ ref('stg_orders') }}
GROUP BY customer_id

