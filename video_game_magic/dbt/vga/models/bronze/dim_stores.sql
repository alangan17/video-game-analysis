{{ config(
    materialized='incremental',
    unique_key='game_store_id',
    post_hook=[
        "{{ log_row_count() }}",
    ],
    tags=[
        "bronze",
        "dimension"
    ]
) }}

with
base as (
    select distinct
        store_id,
        store_name,
        store_slug,
        game_id
    from {{ source('ext_tbl', 'external_stores') }}
),

add_unique_key as (
    select
        *,
        {{ dbt_utils.generate_surrogate_key([
            'game_id',
            'store_id'
        ]) }} as game_store_id
    from base
),

final as (
    select *
    from add_unique_key
)

select *
from final
