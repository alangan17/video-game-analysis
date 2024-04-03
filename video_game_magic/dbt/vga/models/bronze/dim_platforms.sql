{{ config(
    materialized='incremental',
    unique_key='game_platform_id',
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
        platform_id,
        platform_name,
        platform_slug,
        game_id
    from {{ source('ext_tbl', 'external_platforms') }}
),

add_unique_key as (
    select
        *,
        {{ dbt_utils.generate_surrogate_key([
            'game_id',
            'platform_id'
        ]) }} as game_platform_id
    from base
),

final as (
    select *
    from add_unique_key
)

select *
from final
