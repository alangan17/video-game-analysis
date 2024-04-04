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
        "gold",
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

    parent_platform as (
        select
        {{ dbt_utils.star(
            from=ref('dim_parent_platforms')
        ) }}
            from {{ ref('dim_parent_platforms') }}
        ),

        has_metacritic as (
            select *
            from base
            where
                1 = 1
                and metacritic is not null
        ),

        release_join_parent_platform as (
            select
                r.*,
                p.parent_platform_name as platform_name
            from has_metacritic as r
            left join parent_platform as p
                on
                    1 = 1
                    and r.game_id = p.game_id
        ),

        final as (
            select
                release_year,
                release_month,
                release_year_month,
                released,

                platform_name,

                metacritic,
                game_id
            from release_join_parent_platform
        )

        select *
        from final
