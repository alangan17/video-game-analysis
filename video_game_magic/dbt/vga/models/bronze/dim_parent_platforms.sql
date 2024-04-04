{{ config(
    materialized='incremental',
    unique_key='game_parent_platform_id',
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
        platform_id as parent_platform_id,
        platform_name as parent_platform_name,
        platform_slug as parent_platform_slug,
        game_id
    from {{ source('ext_tbl', 'external_parent_platforms') }}
),

add_unique_key as (
    select
        *,
        {{ dbt_utils.generate_surrogate_key([
            'game_id',
            'parent_platform_id'
        ]) }} as game_parent_platform_id
    from base
),

final as (
    select *
    from add_unique_key
)

select *
from final
