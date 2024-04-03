{{ config(
    materialized='table',
    post_hook=[
        "{{ log_row_count() }}",
    ],
    partition_by={
      "field": "released",
      "data_type": "DATE",
      "granularity": "YEAR"
    },
    tags=[
        "bronze",
        "fact"
    ]
) }}

with
base as (
    select
        {{ dbt_utils.star(
            from=source('ext_tbl', 'external_games'),
            except=[
                'slug',
                'name',
                'added',
                'playtime',
                'rating_top',
                'saturated_color',
                'dominant_color'
            ]
        ) }}
        from {{ source('ext_tbl', 'external_games') }}
    ),

    convert_released as (
        select
            game_id,
            tba,
            rating,
            ratings_count,
            metacritic,
            reviews_text_count,
            suggestions_count,
            parse_timestamp('%Y-%m-%dT%H:%M:%S', updated) as updated,
            reviews_count,
            parse_date('%Y-%m-%d', released) as released
        from base
    ),

    final as (
        select *
        from convert_released
    )

    {{ dbt_utils.deduplicate(
        relation='final',
        partition_by='game_id',
        order_by='released desc',
    )
    }}
