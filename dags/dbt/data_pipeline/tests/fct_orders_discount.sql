select
    *
from
    {{ ref('fct_orders') }}
where
    total_discounted_amount < 0
    and (
        date(order_date) > CURRENT_DATE()
        or date(order_date) < '1992-01-01'
    )