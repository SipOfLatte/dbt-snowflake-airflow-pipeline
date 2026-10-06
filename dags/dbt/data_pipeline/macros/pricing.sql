{% macro discounted_amount(extended_price, discount_percent, scale=2) %}
    ({{ extended_price }} * (1 - {{ discount_percent }} / 100))::decimal(16, {{ scale }})
{% endmacro %}