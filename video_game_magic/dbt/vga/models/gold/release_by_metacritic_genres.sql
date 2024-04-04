{{ config(
    materialized='table',
    partition_by={
      "field": "released",
      "data_type": "date",
      "granularity": "month"
    },
    cluster_by = "game_id",
    post_hook=[
        "{{ log_row_count() }}",
    ],
    tags=[
        "silver",
        "fact"
    ]
) }}

with
base as (
    select
        {{ dbt_utils.star(
            from=ref('fact_release_by_yyyymm')
        ) }}
        from {{ ref('fact_release_by_yyyymm') }}
    ),

    genres as (
        select
        {{ dbt_utils.star(
            from=ref('dim_genres')
        ) }}
            from {{ ref('dim_genres') }}
        ),

        has_metacritic as (
            select *
            from base
            where
                1 = 1
                and metacritic is not null
        ),

        release_join_genres as (
            select
                r.*,
                g.genre_name
            from has_metacritic as r
            left join genres
                as g on 1 = 1
            and r.game_id = g.game_id
        ),

        final as (
            select
                release_year,
                release_month,
                release_year_month,
                released,

                genre_name,

                metacritic,
                game_id
            from release_join_genres
        )

        select *
        from final
