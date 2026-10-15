select
    order_key,
    sum(extended_price) as gross_item_sales_amount,
    sum(discounted_amount) as total_discounted_amount
from
    {{ ref('int_order_items') }}
group by
    order_key