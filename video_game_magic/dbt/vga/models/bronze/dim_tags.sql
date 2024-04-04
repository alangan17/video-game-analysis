{{ config(
    materialized='incremental',
    unique_key='game_tag_id',
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
        id as tag_id,
        name as tag_name,
        slug as tag_slug,
        game_id
    from {{ source('ext_tbl', 'external_tags') }}
    where 1=1
    and language = 'eng'
),

add_unique_key as (
    select
        *,
        {{ dbt_utils.generate_surrogate_key([
            'game_id',
            'tag_id'
        ]) }} as game_tag_id
    from base
),

final as (
    select *
    from add_unique_key
)

select *
from final
