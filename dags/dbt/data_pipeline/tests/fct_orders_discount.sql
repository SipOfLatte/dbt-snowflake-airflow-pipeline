select
    *
from
    {{ ref('fct_orders') }}
where
    total_discounted_amount < 0
    or date(order_date) > current_date()
    or date(order_date) < '1992-01-01'
