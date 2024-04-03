{% macro log_row_count() %}

{%- call statement('count_order_items', fetch_result=True) -%}
    SELECT count(*) as count from {{ this }}
{%- endcall -%}

{%- set total_order_items = load_result('count_order_items') -%}

{% if execute %}
    {{ log(modules.datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') ~ ' | ' ~ total_order_items['data'][0][0] ~ ' row(s) transformed', True) }}
{% endif %}

select 1

{% endmacro %}