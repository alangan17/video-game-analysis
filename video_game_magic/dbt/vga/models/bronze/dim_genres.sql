{{ config(
    materialized='incremental',
    unique_key='game_genre_id',
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
        id as genre_id,
        name as genre_name,
        slug as genre_slug,
        game_id
    from {{ source('ext_tbl', 'external_genres') }}
),

add_unique_key as (
    select
        *,
        {{ dbt_utils.generate_surrogate_key([
            'game_id',
            'genre_id'
        ]) }} as game_genre_id
    from base
),

final as (
    select *
    from add_unique_key
)

select *
from final
