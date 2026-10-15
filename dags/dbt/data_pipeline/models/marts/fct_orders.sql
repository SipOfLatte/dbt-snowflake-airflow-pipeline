select
    orders.order_key,
    orders.customer_key,
    orders.order_date,
    orders.order_status,
    orders.order_priority,
    orders.total_price,
    order_items_summary.gross_item_sales_amount,
    order_items_summary.total_discounted_amount
from
    {{ ref('stg_tpch_orders') }} as orders
left join
    {{ ref('int_order_items_summary') }} as order_items_summary
    on orders.order_key = order_items_summary.order_key
