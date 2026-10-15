{% macro discounted_amount(extended_price, discount_rate, scale=2) %}
    ({{ extended_price }} * (1 - {{ discount_rate }}))::decimal(16, {{ scale }})
{% endmacro %}
