{{ config(
    materialized='incremental',
    unique_key='game_id',
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
        game_id,
        slug as game_slug,
        name as game_name
    from {{ source('ext_tbl', 'external_games') }}
),

final as (
    select *
    from base
)

select *
from final
