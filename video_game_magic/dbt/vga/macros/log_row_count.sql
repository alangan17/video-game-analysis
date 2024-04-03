{% macro log_row_count() %}

{%- call statement('get_row_count', fetch_result=True) -%}
    SELECT count(*) as count from {{ this }}
{%- endcall -%}

{%- set row_count = load_result('get_row_count') -%}

{% if execute %}
    {{ log(modules.datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') ~ ' | ' ~ row_count['data'][0][0] ~ ' row(s) transformed', True) }}
{% endif %}

select 1

{% endmacro %}