select
    line_items.line_item_key,
    line_items.order_key,
    line_items.part_key,
    line_items.supplier_key,
    line_items.line_number,
    orders.customer_key,
    orders.order_date,
    orders.order_status,
    orders.order_priority,
    orders.total_price,
    line_items.quantity,
    line_items.extended_price,
    line_items.discount_rate,
    line_items.tax_rate,
    line_items.return_flag,
    line_items.line_status,
    line_items.ship_date,
    line_items.commit_date,
    line_items.receipt_date,
    line_items.ship_instruct,
    line_items.ship_mode,
    line_items.comment,
    {{ discounted_amount('line_items.extended_price', 'line_items.discount_rate') }} as discounted_amount
from
    {{ ref('stg_tpch_orders') }} as orders
join
    {{ ref('stg_tpch_line_items') }} as line_items
    on orders.order_key = line_items.order_key
